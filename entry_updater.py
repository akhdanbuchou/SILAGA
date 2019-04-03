import base64
import json
import time
import urllib.request as urllib2
import urllib
from datetime import datetime
from datetime import timedelta  
from xml.etree.ElementTree import fromstring

import requests
import classifier_rest as classifier
import hbase_rest as hbase 

from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__,static_folder='docx')
CORS(app)

ROW_PER_ITERATION = 2
current_row = 0
DEFAULT_LOG_FILE_NAME = './log/log-classifier-'

# DELAY = 5*60
SOLR = 'http://localhost:8983/'
IP_CLASSIFIER = 'http://localhost:18881/'

# def test_periodic_call():
#     print("updating category ", time.ctime())
#     query = '{}/update'.format(CLASSIFIER_HOST)
#     response = eval(query.read())




def main_helper(start, prev_loc):
    print('mulai dari {}, mengambil {} data'.format(start, ROW_PER_ITERATION))
    #print('sisa lokasi : {}'.format(prev_loc))
    '''
    @param:start adalah row iterasi dimulai 
    @param:prev_loc adalah lokasi yang masih tersisa dari iterasi sebelumnya 
    #1 mengambil data dari solr : online_media 
    #2 klasifikasi berita tsb 
    #3 ambil konten dari hbase : online_media
    #4 simpan di solr : omed_classified
    #5 kalau datanya habis, ditandai dengan len(docs)<row_per_iterate -> jalanin dari awal lagi 
    '''
    #1
    URI = '{}solr/online_media/select?indent=on&q=*:*&rows={}&start={}&wt=python'.format(SOLR, ROW_PER_ITERATION, start)
    # URI = "http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*limit=1]&indent=on&q=keywords:*&rows=2&wt=json&sort=timestamp%20desc"
    connection = urllib2.urlopen(URI) 
    response = eval(connection.read())

    print(URI)
    print(response)

    docs = response['response']['docs']
    numfound = response['response']['numFound']

    loc = prev_loc
    for doc in docs:
        
        try: 
            if doc['entity'][0] == 'LOCATION':
                loc.append(doc['value']) 
        except:
            pass 

        print(doc['id'].split('_'))
        if len(doc['id'].split('_')) < 2:
            print('{}/{}'.format(start, ROW_PER_ITERATION))
            # print('data induk di iterasi ke {}'.format(start/ROW_PER_ITERATION + 1))
            if len(loc)==0:
                loc = ['-']
            author = '-'
            try:
                author = doc['author'][0]
            except:
                pass

            #2
            kategori = classifier.classify(doc['keywords'])

            new_dict = {
                'id':doc['id'],
                'kategori':kategori,
                'url':doc['url'],
                'sitename':doc['sitename'],
                'title':doc['title'],
                'author':author,
                'lokasi':loc,
                'language':doc['language'],
                'timestamp':doc['timestamp'],
                'sentiment':doc['sentiment'],
                'content':''
            }

            #3
            isi = hbase.get_isi_news(doc['id'])
            new_dict['content']=isi
            
            loc = []
            #4
            add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified

    # selesai,lanjutkan ke start berikutnya dengan membawa loc sisa
    print('selesai, lanjutkan ke row {}'.format(start + ROW_PER_ITERATION))
    # main_helper(start + ROW_PER_ITERATION, loc)
    return start + ROW_PER_ITERATION

def add_or_update_to_omed_classified(bulk): # checked 
    '''
    fungsi insert atau update ke solr collection : omed_classified
    param type : json
    '''
    data = {}
    # memindakan data dari input web ke data yang akan dimasukkan ke solr : omed_classified
    for k,v in bulk.items():
        if k in ['id','kategori','url','sitename','lokasi','author','title','language','timestamp','content']:
            data[k]=v
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'id':data['id'],
        'author':data['author'],
        'kategori':data['kategori'],
        'url':data['url'],
        'sitename':data['sitename'],
        'title':data['title'],
        'language':data['language'],
        'lokasi':data['lokasi'],
        'timestamp':data['timestamp'],
        'content':data['content']
        }
    #print(json_data)
    data = json.dumps(json_data)
    response = requests.post('{}solr/omed_classified/update/json/docs'.format(SOLR), headers=headers, data=data)
    print(response)
    print()

# online_media & omed_classified
def main_caller():
    print("updating category ", time.ctime())
    global current_row
    current_row = main_helper(current_row, [])
    print(current_row)

def periodic_call_helper():
    # print("helper")
    scheduler = BackgroundScheduler(standalone=True)
    job = scheduler.add_job(main_caller, 'interval', minutes=1, id='id_scheduler')
    try:
        # print("start")
        scheduler.start()
    except (KeyboardInterrupt):
        logger.debug('Got SIGTERM! Terminating...')
        print("EXIT")



class EntryUpdater:
    HOST = 'http://localhost:8983'
    MAX_ROWS_PER_QUERY = 2
    MAX_CHILDREN_ROWS_PER_QUERY = 2

    def __init__(self):
        self.latest_entry_time = None
        self.latest_entry_id = None
        self.on_updating = False
        self.permit_update = True
    '''
    http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*%20limit=1]
    &indent=on&q=timestamp:[2018-12-01T07:03:17Z%20TO%202019-02-01T07:03:17Z]&wt=json

    http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*limit=0]
    &indent=on&q=timestamp:[2018-01-20T23:59:59Z%20TO%202018-01-21T00:59:59Z]%20keywords:*&rows=1000&wt=python&sort=timestamp%20asc

    http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*%20limit=1]&indent=on&q=keywords:*&wt=json&sort=timestamp%20desc

    localhost:8983/solr/online_media/select?fl=*,[child parentFilter=keywords:* limit=100]&indent=on&q=id:b6fc135aa8ad5df17fee3b490832de01&wt=json
    '''

    def set_latest_entry_time(self, input_date):
        self.latest_entry_time = datetime.strptime(
            input_date, '%Y-%m-%d %H:%M:%S'
            )
        return "success"

    def switch_update_off(self):
        self.permit_update = False
        return self.permit_update
    
    def switch_update_on(self):
        self.permit_update = True
        return self.permit_update

    def allow_update(self):
        self.on_updating = True
        return self.on_updating
    
    def halt_update(self):
        self.on_updating = False
        return self.on_updating

    def get_query_time(self, date):
        # print(datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%dT00:00:00Z'))
        try:
            date_strptime = datetime.strptime(date, '%Y-%m-%d')
            date_strftime = date_strptime.strftime('%Y-%m-%dT00:00:00Z')
        except TypeError:
            date_strftime = date.strftime('%Y-%m-%dT00:00:00Z')
        print(date_strftime)
        return date_strftime
    
    def get_query_timespan(self, earlier_date, latest_date):
        # nxt_str = nxt.strftime('%Y-%m-%dT00:00:00Z')
        print('[{}%20TO%20{}]'.format(earlier_date, latest_date))
        return '[{}%20TO%20{}]'.format(earlier_date, latest_date)

    def convert_datetime(self, input_datetime):
        input_datetime = datetime.strptime(input_datetime,'%Y/%m/%d %H:%M:%S')
        return input_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    def convert_datetime_to_string(self, input_datetime):
        print(input_datetime)
        return input_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    def get_earliest_entry_time(self):
        URI = 'http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*%20limit=1]&indent=on&q=keywords:*&wt=python&rows=1&sort=timestamp%20asc'
        connection = urllib2.urlopen(URI) 
        response = eval(connection.read())

        docs = response['response']['docs']
        timestamp = docs[0]['timestamp']

        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')

    # def update_entry(self, current_first_entry_id=None, current_first_entry_time=None, 
        # next_entry_id=None, next_entry_time=None):
        # print(current_first_entry_time, " ", self.latest_entry_time)
        # print('mulai dari {}, mengambil {} data'.format(start, ROW_PER_ITERATION))
        #print('sisa lokasi : {}'.format(prev_loc))
        '''
        @param:start adalah row iterasi dimulai 
        @param:prev_loc adalah lokasi yang masih tersisa dari iterasi sebelumnya 
        #1 mengambil data dari solr : online_media 
        #2 klasifikasi berita tsb 
        #3 ambil konten dari hbase : online_media
        #4 simpan di solr : omed_classified
        #5 kalau datanya habis, ditandai dengan len(docs)<row_per_iterate -> jalanin dari awal lagi 
        '''
        #1

        if self.latest_entry_time == None:
            print("latest_entry_time NONE")
            q = '&q=keywords:*'
            self.latest_entry_time = datetime.now()
        else:
            print("latest_entry_time not NONE")
            if current_first_entry_time == None:
                earlier_date = self.latest_entry_time
            else:
                earlier_date = next_entry_time

            startdate = self.get_query_time(datetime.now())
            timespan = self.get_query_timespan(earlier_date, startdate)
            q = '&q=timestamp:{}%20keywords:*'.format(timespan)
        print("inside update entry")
        # URI = '{}solr/online_media/select?indent=on&q=*:*&rows={}&start={}&wt=python'.format(SOLR, ROW_PER_ITERATION, start)
        URI = '{}/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*limit=0]&indent=on{}&rows={}&wt=python&sort=timestamp%20desc'.format(
            self.HOST, q, str(self.MAX_ROWS_PER_QUERY)
            )
        print(URI)

        # URI = "http://localhost:8983/solr/online_media/select?indent=on&q=*:*&rows=2&start=0&wt=python"

        # print(URI)
        # return URI
        
        connection = urllib2.urlopen(URI) 
        response = eval(connection.read())
        # print(response)

        docs = None
        numFound = None
        try:
            docs = response['response']['docs']
            numFound = response['response']['numFound']
        except: 
            pass
        # print(numFound)

        ##skenario tanggal yang sama
        if current_first_entry_id != None:
            for ii in range(len(docs)):
                if docs[ii]['id'] == next_entry_id:
                    docs = docs[ii+1:]
                    break

        # loc = prev_loc
        for doc in docs:
            if self.latest_entry_id == doc['id']:
                break
            elif self.latest_entry_id == None:
                self.latest_entry_id = doc['id']

            if current_first_entry_id == None:
                current_first_entry_id = doc['id']
                current_first_entry_time = doc['timestamp']

            # print(doc['id'])
            q_parent_id = '&q=id:{}'.format(doc['id'])
            children_URI = '{}/solr/online_media/select?fl=[child%20parentFilter=keywords:*%20limit={}]&indent=on{}&wt=python'.format(
            self.HOST, self.MAX_CHILDREN_ROWS_PER_QUERY, q_parent_id
            )

            # print(children_URI)

            children_connection = urllib2.urlopen(children_URI) 
            children_responses = eval(children_connection.read())
            # print(children_responses)
            children_docs = children_responses['response']['docs'][0]['_childDocuments_']
            # print(children_docs)
            loc = list()
            for children_doc in children_docs:
                try: 
                    if children_doc['entity'][0] == 'LOCATION':
                        loc.append(children_doc['value']) 
                except:
                    pass 

            if len(loc)==0:
                loc = ['-']
            
            try:
                author = doc['author'][0]
            except:
                author = '-'
            print(loc)
            #2
            kategori = classifier.classify(doc['keywords'])
            # print(kategori)

            new_dict = {
                'id':doc['id'],
                'kategori':kategori,
                'url':doc['url'],
                'sitename':doc['sitename'],
                'title':doc['title'],
                'author':author,
                'lokasi':loc,
                'language':doc['language'],
                'timestamp':doc['timestamp'],
                'sentiment':doc['sentiment'],
                'content':''
            }

            print(new_dict['id'])
            print(doc['id'])

            #3
            
            '''uncomment later'''
            isi = hbase.get_isi_news(doc['id'])
            new_dict['content']=isi
            
            
            # loc = []
            #4
            # add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified
            next_entry_id = doc['id']
            next_entry_time = doc['timestamp']
        print(next_entry_id, "entry id - entry time ", next_entry_time)
                

        # selesai,lanjutkan ke start berikutnya dengan membawa loc sisa
        # print('selesai, lanjutkan ke row {}'.format(start + ROW_PER_ITERATION))
        # main_helper(start + ROW_PER_ITERATION, loc)
        # return start + ROW_PER_ITERATION
        return numFound, current_first_entry_id, current_first_entry_time, next_entry_id, next_entry_time

    def update_entry2(self, earlier_time, later_time, interval, sort='desc'):
        
        '''
        @param:start adalah row iterasi dimulai 
        @param:prev_loc adalah lokasi yang masih tersisa dari iterasi sebelumnya 
        #1 mengambil data dari solr : online_media 
        #2 klasifikasi berita tsb 
        #3 ambil konten dari hbase : online_media
        #4 simpan di solr : omed_classified
        #5 kalau datanya habis, ditandai dengan len(docs)<row_per_iterate -> jalanin dari awal lagi 
        '''
        #1

        if earlier_time > later_time:
            earlier_time, later_time = later_time, earlier_time

        start_date = self.convert_datetime_to_string(earlier_time)
        end_date = self.convert_datetime_to_string(later_time)
        timespan = self.get_query_timespan(start_date, end_date)
        q = '&q=timestamp:{}'.format(timespan)
        
        # URI = '{}solr/online_media/select?indent=on&q=*:*&rows={}&start={}&wt=python'.format(SOLR, ROW_PER_ITERATION, start)
        URI = '{}/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*limit=0]&indent=on{}&rows={}&wt=python&sort=timestamp%20{}'.format(
            self.HOST, q, self.MAX_ROWS_PER_QUERY, sort
            )

        # URI = "http://localhost:8983/solr/online_media/select?indent=on&q=*:*&rows=2&start=0&wt=python"

        # print(URI)
        # return URI
        
        connection = urllib2.urlopen(URI) 
        response = eval(connection.read())

            
        # print(response)

        # docs = None
        # numFound = None
        try:

            numFound = response['response']['numFound']

            if numFound > self.MAX_ROWS_PER_QUERY:
                URI = '{}/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*limit=0]&indent=on{}&rows={}&wt=python&sort=timestamp%20{}'.format(
                    self.HOST, q, numFound, sort
                    )
                connection = urllib2.urlopen(URI) 
                response = eval(connection.read())
                
            print(URI)
            print(numFound)
            docs = response['response']['docs']
            
        except: 
            pass

        for doc in docs:
            if  not self.on_updating:
                return
            try:
                current_entry_timestamp = datetime.strptime(doc['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
                if  self.permit_update and (self.latest_entry_time == None or self.latest_entry_time < current_entry_timestamp) :
                    self.latest_entry_time = current_entry_timestamp

                # print('new latest entry time')
            except:
                pass

            # print(doc['id'])
            q_parent_id = '&q=id:{}'.format(doc['id'])
            children_URI = '{}/solr/online_media/select?fl=[child%20parentFilter=keywords:*%20limit={}]&indent=on{}&wt=python'.format(
                self.HOST, self.MAX_CHILDREN_ROWS_PER_QUERY, q_parent_id
                )

            children_connection = urllib2.urlopen(children_URI) 
            children_responses = eval(children_connection.read())
            
            # print(children_responses)
            children_docs = children_responses['response']['docs'][0]['_childDocuments_']
            # print(children_docs)
            loc = list()
            for children_doc in children_docs:
                try: 
                    if children_doc['entity'][0] == 'LOCATION':
                        loc.append(children_doc['value']) 
                except:
                    pass 

            if len(loc)==0:
                loc = ['-']
            
            try:
                author = doc['author'][0]
            except:
                author = '-'
            try:
                language = doc['language']
            except:
                language = ''
            try:
                sentiment = doc['sentiment']
            except:
                sentiment = ''
            # print(loc)
            #2
            kategori = classifier.classify(doc['keywords'])
            # print(kategori)

            new_dict = {
                'id':doc['id'],
                'kategori':kategori,
                'url':doc['url'],
                'sitename':doc['sitename'],
                'title':doc['title'],
                'author':author,
                'lokasi':loc,
                'language':language,
                'timestamp':doc['timestamp'],
                'sentiment':sentiment,
                'content':''
            }


            print(doc['id'])

            #3
            
            isi = hbase.get_isi_news(doc['id'])
            new_dict['content']=isi
            
            log_write(timespan, '-', doc['timestamp'], ':', doc['id'])
            
            #4
            # add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified
            next_entry_id = doc['id']
            next_entry_time = doc['timestamp']
                
        return 


    def updater_helper(self, earlier_time_input, later_time_input, time_interval):
        self.allow_update()
        self.switch_update_off()

        if time_interval > 0:
            sort = 'asc'
            basic_time = earlier_time_input
            limit_time = later_time_input
            operation = 1
        else:
            sort = 'desc'
            basic_time = later_time_input
            limit_time = earlier_time_input
            operation = -1

        limit_time = datetime.strptime(limit_time,'%Y/%m/%d %H:%M:%S')
        next_entry_time = basic_time = datetime.strptime(basic_time,'%Y/%m/%d %H:%M:%S')
        next_entry_time += operation*timedelta(hours=abs(time_interval))
        condition = True
        while condition:
            self.update_entry2(basic_time, next_entry_time, time_interval, sort)
            condition = False if ((next_entry_time > limit_time and operation > 0) or (next_entry_time < limit_time and operation < 0)) else True
            basic_time = next_entry_time
            next_entry_time += operation*timedelta(hours=abs(time_interval))
        
        self.halt_update()
        self.switch_update_on()
        return


    def periodic_updater_helper(self, time_interval_hours=1, time_interval_weeks=54/2):
        if not self.on_updating and self.permit_update:
            # print( "Will update: ", self.permit_update and not self.on_updating)
            self.allow_update()
        else:
            print("...NOT UPDATING...") 
            return

        if self.latest_entry_time == None:
            delta_time = timedelta(weeks=abs(time_interval_weeks))
            earlier_time = self.get_earliest_entry_time()
        else:
            delta_time = timedelta(hours=abs(time_interval_hours))
            earlier_time = self.latest_entry_time

        sort = 'asc'
        # next_entry_time = basic_time = datetime.strptime(basic_time,'%Y/%m/%d %H:%M:%S')
        limit_time = datetime.now()
        # print(earlier_time, " | ", limit_time, " | ", self.on_updating)
        next_entry_time = earlier_time
        next_entry_time += delta_time
        condition = True
        while condition and self.on_updating and self.permit_update:
            # print("condition true ", self.on_updating and self.permit_update)
            self.update_entry2(earlier_time, next_entry_time, time_interval_hours, sort)
            condition = False if (next_entry_time > limit_time) else True
            earlier_time = next_entry_time
            next_entry_time += delta_time

        self.halt_update()
        return
        

def log_write(*args):
    current_time = datetime.now()
    current_time_day = current_time.strftime('%Y-%m-%d')
    current_time_clock = current_time.strftime('[%H:%M:%S]')
    f= open(DEFAULT_LOG_FILE_NAME + current_time_day +'.txt',"a+")
    log_input = "{} --- ".format(current_time_clock)
    for arg in args:
        log_input += arg + ' '
    log_input += '\n'
    f.write(log_input)
    f.close() 