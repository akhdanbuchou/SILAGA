import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import json
import base64
import urllib.request as urllib2
from datetime import datetime
import time
import mysql_rest as mysql
import solr_rest as solr
import hashlib

def b64decode(b): # basis 64 decoder
    return base64.b64decode(b)

def bdecode(b): # byte to string decoder 
    return b.decode('utf-8')

def bungkus(s):
    return bdecode(b64encode(sencode(s)))

def sencode(s):
    return s.encode()

def b64encode(b):
    return base64.b64encode(b)

def get_all_online_media(list_id):
    '''
    mengembalikan json data berita dari hbase online_media : id, judul, lokasi, isi, kategori, timestamp
    param : list id berita di solr 
    '''
    list_berita_hbase = []
    headers = {
        'Accept': 'application/json',
    }
    for lst in list_id:
        id_berita=lst[0]
        lokasi=lst[1]
        response = requests.get('http://localhost:4444/online_media/' + id_berita, headers=headers)
        text64 = response.text
        data = json.loads(text64)
        #list of values
        val = {}
        val['id'] = bdecode(b64decode(data["Row"][0]["key"]))
        cells = data['Row'][0]['Cell']
        val['lokasi'] = lokasi
        val['kategori'] = 'netral'
        for v in cells:
            col = b64decode(v['column'])
            cold = bdecode(col)
            con = b64decode(v['$'])
            cond = bdecode(con)
            if "timestamp" in cold:
                val['timestamp'] = cond
            if "title" in cold:
                val['judul'] = cond
            if "content" in cold:
                val['isi'] = cond
        list_berita_hbase.append(val)
    return list_berita_hbase

def put_online_media(bulk):
    '''
    insert data ke hbase online_media
    param : json (author, content, language, sitename, url)
    '''
      
    data = {}
    # memindakan data dari input web ke data yang akan dimasukkan ke hbase : online_media
    for k,v in bulk.items():
        if k in ["author","title","content","language","sitename","url","id"]:
            data[k]=v

    # preparing data yang akan dimasukkan ke hbase, menyesuaikan struktur data 
    ts =int(time.time()) 
    id_news = data["id"]
    result = {"Row":[{"key":id_news,"Cell":[]}]}
    cell = [] # nantinya akan dimasukkan ke Cell 
    for k,v in data.items():
        col = {}
        column = 'nodejs:' + k
        value = v
        col['column'] = bungkus(column)
        col['timestamp'] = ts
        col['$'] = bungkus(value)
        cell.append(col)
    result['Row'][0]['Cell'] = cell
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    print(result)
    data = json.dumps(result)
    # post using culr to hbase 
    response = requests.put('http://localhost:4444/online_media/'+id_news, headers=headers, data=data)
    print(response)
    print("success adding to hbase : online_media")


