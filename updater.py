import base64
import json
import time
import urllib.request as urllib2
from datetime import datetime
from xml.etree.ElementTree import fromstring

import requests
import classifier_rest as classifier
import hbase_rest as hbase 

ROW_PER_ITERATION = 10000
DELAY = 5*60
SOLR = 'http://localhost:8983/'
IP_CLASSIFIER = 'http://localhost:18881/'

# online_media & omed_classified
def main():
    main_helper(0, [])

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
    main_helper(start + ROW_PER_ITERATION, loc)

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

if __name__=='__main__':
    main()