import base64
import json
import time
import urllib.request as urllib2
from datetime import datetime
from xml.etree.ElementTree import fromstring

import requests
from xmljson import badgerfish as bf

import classifier_rest as classifier
import hbase_rest as hbase
import mysql_rest as mysql

ROW_NUM = 10000
HOST = 'http://localhost:3333/'

# online_media & omed_classified

def classify_online_media_and_store_to_omed_classified(): #checked
    '''
    mengambil data dari online_media, klasifikasi, dan menyimpan ke omed_classified
    '''
    connection = urllib2.urlopen(HOST + 'solr/online_media/select?indent=on&q=*:*&rows='+str(ROW_NUM)+'&wt=python') 
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
            isi = hbase.get_isi_news(doc['id'])
            new_dict['content']=isi
            list_id_berita.append(new_dict)
            loc = []
            add_or_update_to_omed_classified(new_dict) # store it in solr : omed_classified

# solr : online_media RELATED

def getNumFound_online_media():
    '''
    mengembalikan jumlah data di online_media
    '''
    connection = urllib2.urlopen(HOST + 'solr/online_media/select?indent=on&q=*:*&rows=10&wt=python')
    response = eval(connection.read())
    numfound = response['response']['numFound']
    return numfound

def get_all_online_media_id(): # checked
    '''
    mengembalikan semua id berita dan 1 lokasi di solr collection : online_media
    '''
    connection = urllib2.urlopen(HOST + 'solr/online_media/select?indent=on&q=*:*&rows=' + str(ROW_NUM) + '&wt=python')
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

# omed_classified RELATED

def getNumFound_omed_classified():
    '''
    mengembalikan jumlah dokumen di omed_classified
    '''
    connection = urllib2.urlopen(HOST + 'solr/omed_classified/select?indent=on&q=*:*&rows=1&wt=python')
    response = eval(connection.read())
    numfound = response['response']['numFound']
    return numfound

def get_all_omed_classified():
    '''
    mengembalikan semua berita dari solr : omed_classified
    '''
    num = getNumFound_omed_classified()
    connection = urllib2.urlopen(HOST + 'solr/omed_classified/select?indent=on&q=*:*&rows=' + str(num) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        # olah bagian kategori
        # print('{} {}'.format(doc['id'], doc['kategori']))
        kat = doc['kategori'][0]
        kat_name = classifier.get_category_name(kat)
        doc['timestamp'] = str(doc['timestamp'])[0:10] + " "+str(doc['timestamp'])[11:19]
        doc['kategori'] = kat_name # override 
        doc['content'] = doc['content'][0]
        doc['title'] = doc['title'][0]
    return docs

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
    print(json_data)
    data = json.dumps(json_data)
    response = requests.post(HOST + 'solr/omed_classified/update/json/docs', headers=headers, data=data)
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
    response = requests.post(HOST + 'solr/omed_classified/update', headers=headers, params=params, data=data)
    print(response)

def delete_all_omed_classified():
    '''
    menghapus semua data di omed_classified
    '''
    num = getNumFound_omed_classified()
    lst = []
    connection = urllib2.urlopen(HOST + 'solr/omed_classified/select?indent=on&q=*:*&rows=10'+str(num)+'&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        lst.append(doc['id'])

    for i in lst: #hapus
        delete_from_omed_classified(i)

# TELEGRAM RELATED

def getNumFound_telegram():
    '''
    mengembalikan jumlah dokumen di telegram
    '''
    connection = urllib2.urlopen(HOST + 'solr/telegram/select?indent=on&q=*:*&rows=1&wt=python')
    response = eval(connection.read())
    numfound = response['response']['numFound']
    return numfound

def add_or_update_to_telegram(data): # ON PROGRESS 
    '''
    fungsi insert atau update ke solr collection : telegram
    param type : json
    '''
    headers = {
        'Content-Type': 'application/json',
    }
    print(data)
    data = json.dumps(data)
    response = requests.post(HOST + 'solr/telegram/update/json/docs', headers=headers, data=data)
    print(response)
    
def get_all_telegram_reports():
    '''
    mengembalikan semua berita dari solr : telegram
    '''
    num = getNumFound_telegram()
    connection = urllib2.urlopen(HOST + 'solr/telegram/select?indent=on&q=*:*&rows=' + str(num) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    result = []
    for doc in docs:
        res = {}
        kat = doc['kategori'][0]
        kat_name = classifier.get_category_name(kat)
        res['timestamp'] = str(doc['date'][0])[0:10] + " "+str(doc['date'][0])[11:19]
        res['kategori'] = kat_name # override 
        res['pelapor'] = doc['pelapor'][0]
        res['content'] = doc['laporan'][0]
        res['id'] = doc['id']
        result.append(res)
    return result

def delete_from_telegram(id_report):
    '''
    fungsi delete row dengan id=id_report dari solr collection : telegram
    '''
    headers = {
        'Content-Type': 'text/xml',
    }
    params = (
        ('commit', 'true'),
    ) 
    data = '<delete><id>'+id_report+'</id></delete>'
    response = requests.post(HOST + 'solr/telegram/update', headers=headers, params=params, data=data)
    print(response)

