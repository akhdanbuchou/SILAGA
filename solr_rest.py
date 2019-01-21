import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import json
import base64
import urllib.request as urllib2
from datetime import datetime
import time
import mysql_rest as mysql
import classifier_rest as classifier 

ROW_NUM = 3000

def classify_and_store_to_omed_classified():
    connection = urllib2.urlopen('http://localhost:3333/solr/online_media/select?indent=on&q=*:*&rows='+str(ROW_NUM)+'&wt=python') # coba 10.000 row
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        if len(doc['id'].split('_')) < 2:
            kategori = classifier.classify(doc['keywords']) # clasify it 
            new_dict = {
                'id':doc['id'],
                'kategori':kategori
            }
            add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified

def get_all_online_media_id():
    '''
    mengembalikan semua id berita dan 1 lokasi di solr collection : online_media
    '''
    connection = urllib2.urlopen('http://localhost:3333/solr/online_media/select?indent=on&q=*:*&rows=' + str(ROW_NUM) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    list_id_berita = []
    loc = []
    for doc in docs: 
        try:
            if doc['entity'][0] == 'LOCATION':
                loc.append(doc['value']) 
        except:
            pass   
        if len(doc['id'].split('_')) < 2:
            new_dict = {
                'id':doc['id'],
                'lokasi':loc[0][0],
                'url':doc['url'][0],
                'sitename':doc['sitename'][0],
                'author':doc['author'][0]
                }
            list_id_berita.append(new_dict)
            loc = []
    return list_id_berita

def get_all_online_media():
    '''
    mengembalikan semua data json berita di solr collection : online_media
    '''
    connection = urllib2.urlopen('http://localhost:3333/solr/online_media/select?indent=on&q=*:*&rows=' + str(ROW_NUM) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    list_berita = []
    loc = []
    for doc in docs:
        # menangkap lokasi
        try:
            if doc['entity'][0] == 'LOCATION':
                loc.append(doc['value']) 
        except:
            pass

        if len(doc['id'].split('_')) < 2:
            new_dict = {'id': doc['id'],
                        'loc': loc,
                        'time': doc['timestamp'],
                        'author':doc['author'],
                        'url':doc['url'],
                        'sitename':doc['sitename'],
                        }
            list_berita.append(new_dict)
            print(new_dict)
            print()
            loc = []
    return list_berita

def add_or_update_to_omed_classified(bulk):
    '''
    fungsi insert atau update ke solr collection : omed_classified
    param type : json
    '''
    data = {}
    # memindakan data dari input web ke data yang akan dimasukkan ke solr : omed_classified
    for k,v in bulk.items():
        if k in ["id","kategori"]:
            data[k]=v
    print(data['id'])
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        "id":data['id'],
        "category":data['kategori']
        }
    data = json.dumps(json_data)
    response = requests.post('http://localhost:3333/solr/omed_classified/update/json/docs', headers=headers, data=data)
    print(response)
    print("success adding to solr : omed_classified")

def get_keywords_from_news(id_berita):
    '''
    mengembalikan list keywords dari suatu berita yang disimpan di solr 
    '''
    connection = urllib2.urlopen('http://localhost:3333/solr/online_media/select?q=id:'+id_berita+'&wt=python')
    response = eval(connection.read())
    doc = response['response']['docs'][0]
    return doc['keywords']

def delete_from_omed_classified(id_berita):
    '''
    fungsi delete row dengan id=id_berita dari solr collection : omed_classified
    '''
    headers = {
        'Content-Type': 'text/xml',
    }
    params = (
        ('commit', 'true'),
    ) 
    data = '<delete><id>'+id_berita+'</id></delete>'
    response = requests.post('http://localhost:3333/solr/omed_classified/update', headers=headers, params=params, data=data)
    print(response)

def get_all_omed_classified():
    '''
    mengembalikan semua data dari solr collection : omed_classified
    '''
    connection = urllib2.urlopen('http://localhost:3333/solr/omed_classified/select?indent=on&q=*:*&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    list_berita = []
    for doc in docs:    
        if len(doc['id'].split('_')) < 2:
            list_berita.append(doc['id'])
    return list_berita



def get_from_omed_classified(id_berita):
    '''
    mengembalikan json data suatu berita di solr collection : omed_classified
    '''
    connection = urllib2.urlopen('http://localhost:3333/solr/omed_classified/select?q=id:'+id_berita+'&wt=python')
    response = eval(connection.read())
    print(str(response['response']['numFound'] )+ " documents found.")
    for doc in response['response']['docs']:
        print(doc)
