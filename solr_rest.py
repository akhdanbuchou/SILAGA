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

ROW_NUM = 10000
HOST = 'http://localhost:3333/solr'

def getNumFound_online_media():
    connection = urllib2.urlopen(HOST + '/online_media/select?indent=on&q=*:*&rows=10&wt=python')
    response = eval(connection.read())
    numfound = response['response']['numFound']
    return numfound

def getNumFOund_omed_classified():
    connection = urllib2.urlopen(HOST + '/omed_classified/select?indent=on&q=*:*&rows=10&wt=python')
    response = eval(connection.read())
    numfound = response['response']['numFound']
    return numfound

def delete_all_omed_classified():
    num = getNumFOund_omed_classified()
    lst = []
    connection = urllib2.urlopen(HOST + '/omed_classified/select?indent=on&q=*:*&rows=10'+str(num)+'&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        lst.append(doc['id'])

    for i in lst: #hapus
        delete_from_omed_classified(i)

def classify_online_media_and_store_to_omed_classified(): #checked
    connection = urllib2.urlopen(HOST + '/online_media/select?indent=on&q=*:*&rows='+str(ROW_NUM)+'&wt=python') 
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
            if len(loc)==0:
                loc = ['-']

            author = '-'

            try:
                author = doc['author'][0]
            except:
                pass
            kategori = classifier.classify(doc['keywords']) # clasify it 
            new_dict = {
                'id':doc['id'],
                'kategori':kategori,
                'url':doc['url'],
                'sitename':doc['sitename'],
                'title':doc['title'],
                'lokasi':loc,
                'language':doc['language'],
                'timestamp':doc['timestamp'],
                'sentiment':doc['sentiment']
            }
            list_id_berita.append(new_dict)
            loc = []
            add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified



def get_all_omed_classified():
    '''
    mengembalikan semua berita dari solr : omed_classified
    '''
    num = getNumFOund_omed_classified()
    connection = urllib2.urlopen(HOST + '/omed_classified/select?indent=on&q=*:*&rows=' + str(num) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        # olah bagian kategori 
        kat = doc['kategori'][0]
        kat_name = classifier.get_category_name(kat)
        doc['kategori'] = kat_name # override 
    return docs

def get_all_online_media_id(): # checked
    '''
    mengembalikan semua id berita dan 1 lokasi di solr collection : online_media
    '''
    connection = urllib2.urlopen(HOST + '/online_media/select?indent=on&q=*:*&rows=' + str(ROW_NUM) + '&wt=python')
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
            if len(loc)==0:
                loc = ['-']

            author = '-'

            try:
                author = doc['author'][0]
            except:
                pass

            new_dict = {
                'id':doc['id'],
                'lokasi':loc[0],
                'url':doc['url'][0],
                'sitename':doc['sitename'][0],
                'author':author
                }
            list_id_berita.append(new_dict)
            loc = []
    return list_id_berita

def add_or_update_to_omed_classified(bulk): # checked 
    '''
    fungsi insert atau update ke solr collection : omed_classified
    param type : json
    '''
    data = {}
    # memindakan data dari input web ke data yang akan dimasukkan ke solr : omed_classified
    for k,v in bulk.items():
        if k in ['id','kategori','url','sitename','lokasi','author','title','language','timestamp','sentiment']:
            data[k]=v
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'id':data['id'],
        'kategori':data['kategori'],
        'url':data['url'],
        'sitename':data['sitename'],
        'title':data['title'],
        'language':data['language'],
        'lokasi':data['lokasi'],
        'timestamp':data['timestamp'],
        'sentiment':data['sentiment']
        }
    print(json_data)
    data = json.dumps(json_data)
    response = requests.post(HOST + '/omed_classified/update/json/docs', headers=headers, data=data)
    print(response)
    print()

def delete_from_omed_classified(id_berita): # checked
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
    response = requests.post(HOST + '/omed_classified/update', headers=headers, params=params, data=data)
    print(response)
