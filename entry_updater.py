import base64
import json
import time
import urllib.request as urllib2
from datetime import datetime
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

DELAY = 5*60
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
    connection = urllib2.urlopen(URI) 
    response = eval(connection.read())

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

    def __init__(self):
        self.last_entry_time = None
        self.last_entry_id = None
    '''
    http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*%20limit=1]
    &indent=on&q=timestamp:[2018-12-01T07:03:17Z%20TO%202019-02-01T07:03:17Z]&wt=json

    http://localhost:8983/solr/online_media/select?fl=*,[child%20parentFilter=keywords:*%20limit=1]&indent=on&q=keywords:*&wt=json&sort=timestamp%20desc
    '''

    def get_query_timespan(self, start, end):
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_end = datetime.strptime(end, '%Y-%m-%d')

        return dt_start, dt_end
    
    def get_query_time_converted(self, now, nxt):
        now_str = now.strftime('%Y-%m-%dT00:00:00Z')
        nxt_str = nxt.strftime('%Y-%m-%dT00:00:00Z')
        return '[{}%20TO%20{}]'.format(now_str, nxt_str)

    def update_entry(self):
        current_first_entry_id = None
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

        if self.last_entry_time == None:
            q = ''
        else:
            dt_start, dt_end = self.get_query_timespan(start,datetime.now())
            startdate = self.get_query_time_converted(now,nxt)
            q = '&q=timestamp:{}'.format(startdate)
        print("inside update entry")
        # URI = '{}solr/online_media/select?indent=on&q=*:*&rows={}&start={}&wt=python'.format(SOLR, ROW_PER_ITERATION, start)
        URI = '{}/solr/online_media/select?fl=*,[child parentFilter=keywords:* limit=1]&indent=on{}&rows=2&wt=json&sort=timestamp desc'.format(self.HOST,q)
        print(URI)
        return URI
        
        # connection = urllib2.urlopen(URI) 
        # response = eval(connection.read())

        # docs = response['response']['docs']
        # numfound = response['response']['numFound']

        # # loc = prev_loc
        # for doc in docs:
        #     if self.last_entry_id == doc['id']:
        #         return

        #     if current_first_entry_id == None:
        #         current_first_entry_id = doc['id']
            
        #     # try: 
        #     #     if doc['entity'][0] == 'LOCATION':
        #     #         loc.append(doc['value']) 
        #     # except:
        #     #     pass 

        #     # print(doc['id'].split('_'))
        #     # if len(doc['id'].split('_')) < 2:
        #     if True:
        #         # print('{}/{}'.format(start, ROW_PER_ITERATION))
        #         # print('data induk di iterasi ke {}'.format(start/ROW_PER_ITERATION + 1))
        #         # if len(loc)==0:
        #         #     loc = ['-']
        #         author = '-'
        #         try:
        #             author = doc['author'][0]
        #         except:
        #             pass

        #         #2
        #         kategori = classifier.classify(doc['keywords'])

        #         new_dict = {
        #             'id':doc['id'],
        #             'kategori':kategori,
        #             'url':doc['url'],
        #             'sitename':doc['sitename'],
        #             'title':doc['title'],
        #             'author':author,
        #             'lokasi':loc,
        #             'language':doc['language'],
        #             'timestamp':doc['timestamp'],
        #             'sentiment':doc['sentiment'],
        #             'content':''
        #         }

        #         print(new_dict)

        #         #3
                
                
        #         isi = hbase.get_isi_news(doc['id'])
        #         new_dict['content']=isi
                
                
        #         loc = []
        #         #4
        #         add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified
                

        # # selesai,lanjutkan ke start berikutnya dengan membawa loc sisa
        # # print('selesai, lanjutkan ke row {}'.format(start + ROW_PER_ITERATION))
        # # main_helper(start + ROW_PER_ITERATION, loc)
        # # return start + ROW_PER_ITERATION
        
        
