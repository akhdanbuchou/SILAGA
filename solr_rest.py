import base64
import json
import time
import urllib.request as urllib2
import urllib
from datetime import datetime
from xml.etree.ElementTree import fromstring

import requests

import hbase_rest as hbase
import mysql_rest as mysql

ROW_NUM = 10000
HOST = 'http://10.32.6.225:8983/'
HOST_CLASSIFIER = 'http://10.32.6.225:18881'

#dev
HOST = 'http://localhost:8983/'
HOST_CLASSIFIER = 'http://localhost:18881'

ITER_NUM = 5

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

def get_omed_with_interval_ALPHA(start):
    if start<30:
        connection = urllib2.urlopen('{}solr/omed_classified/select?indent=on&q=*:*&start={}&rows=5&wt=python'.format(HOST,start))
        response = eval(connection.read())
        docs = response['response']['docs']
        for doc in docs:
            print(doc['timestamp'])
        print()
        get_omed_with_interval_ALPHA(start+5)
    else:
        print('stop')

# omed_classified RELATED

def getNumFound_omed_classified():
    '''
    mengembalikan jumlah dokumen di omed_classified
    '''
    connection = urllib2.urlopen(HOST + 'solr/omed_classified/select?indent=on&q=*:*&rows=1&wt=python')
    response = eval(connection.read())
    numfound = response['response']['numFound']
    return numfound

def get_all_omed_classified(num):
    '''
    mengembalikan semua berita dari solr : omed_classified
    '''
    connection = urllib2.urlopen(HOST + 'solr/omed_classified/select?indent=on&q=*:*&sort=timestamp%20asc&rows=' + str(num) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        # print(doc['timestamp'])
        # olah bagian kategori
        kat = doc['kategori'][0]

        con = urllib2.urlopen(HOST_CLASSIFIER + '/category-name/{}'.format(kat))
        res = eval(con.read())
        kat_name = res['result']

        doc['timestamp'] = str(doc['timestamp'])[0:10] + " "+str(doc['timestamp'])[11:19]
        doc['kategori'] = kat_name # override 
        doc['content'] = doc['content'][0]
        doc['title'] = doc['title'][0]
    return docs

def get_map(jenis, start, end, keyword):
    startdate = '[{}%20TO%20{}]'.format(start, end)
    # keyword 
    
    # kategori like a madman 
    q = ''
    if jenis == '0':
        q = 'kategori:[{}%20TO%20{}]'.format(1, 185)
        idx = 0
    if jenis == '1':
        q = 'kategori:[{}%20TO%20{}]'.format(1, 90)
    if jenis == '2':
        q = 'kategori:[{}%20TO%20{}]'.format(91, 144)
    if jenis == '3':
        q = 'kategori:[{}%20TO%20{}]'.format(145, 167)
    if jenis == '4':
        q = 'kategori:[{}%20TO%20{}]'.format(168, 185)

    # jumlah data dengan filter tersebut 
    test = '{}solr/omed_classified/select?indent=on&q={}&fq=start_date={}&sort=timestamp%20asc&rows=1&wt=python'.format(HOST, q, startdate)
    connection = urllib2.urlopen(test)
    response = eval(connection.read())
    numfound = response['response']['numFound']
    print(numfound)

    # mengambil data 
    location = []
    url = '{}solr/omed_classified/select?indent=on&q={}&fq=start_date={}&sort=timestamp%20asc&rows={}&wt=python'.format(HOST, q, startdate, numfound)
    print(url)
    connection = urllib2.urlopen(url)
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        print(doc['id'])
        print(doc['lokasi'])
        lokasi = doc['lokasi']
        for tempat in lokasi:
            if tempat.capitalize() not in location:
                location.append(tempat.capitalize())
        print()

    print(location)
    return location

def get_pie(jenis, start, end, keyword): # kalau 0 all, selain itu mengikuti 
    startdate = '[{}%20TO%20{}]'.format(start, end)
    # keyword 
    
    # kategori like a madman 
    q = ''
    idx = 1
    if jenis == '0':
        q = 'kategori:[{}%20TO%20{}]'.format(1, 185)
        idx = 0
    if jenis == '1':
        q = 'kategori:[{}%20TO%20{}]'.format(1, 90)
    if jenis == '2':
        q = 'kategori:[{}%20TO%20{}]'.format(91, 144)
    if jenis == '3':
        q = 'kategori:[{}%20TO%20{}]'.format(145, 167)
    if jenis == '4':
        q = 'kategori:[{}%20TO%20{}]'.format(168, 185)

    # jumlah data dengan filter tersebut 
    test = '{}solr/omed_classified/select?indent=on&q={}&fq=start_date={}&sort=timestamp%20asc&rows=1&wt=python'.format(HOST, q, startdate)
    connection = urllib2.urlopen(test)
    response = eval(connection.read())
    numfound = response['response']['numFound']
    # print(numfound)

    # mengambil data 
    result = {}
    url = '{}solr/omed_classified/select?indent=on&q={}&fq=start_date={}&sort=timestamp%20asc&rows={}&wt=python'.format(HOST, q, startdate, numfound)
    # print(url)
    connection = urllib2.urlopen(url)
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        kat_id = doc['kategori'][0]
        con = urllib2.urlopen(HOST_CLASSIFIER + '/category-name/{}'.format(kat_id))
        res = eval(con.read())
        kat_name = res['result'][idx]

        if kat_name not in result:
            result[kat_name] = 1
        else:
            result[kat_name] += 1
    print(result)

    # merapikan data buat dilempar ke Vue
    arr =[]
    for k,v in result.items():
        new_dict = {}
        new_dict['namaGangguan'] = k
        new_dict['jumlahGangguan'] = v
        arr.append(new_dict)
    return arr

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

def get_rekap(level, interval, start, end):
    HARIAN = [0,10]
    BULANAN = [0,7]
    TAHUNAN = [0,4]
    FORMAT_HARIAN = '%Y-%m-%d'
    FORMAT_BULANAN = '%Y-%m'
    FORMAT_TAHUNAN = '%Y'

    print('mengambil rekap data level {} interval {} dari {} sampai {}'.format(level, interval, start, end))

    splitter = []
    format = ''
    print(format)
    if interval=="tahunan":
        splitter=TAHUNAN
        format=FORMAT_TAHUNAN
    elif interval=="bulanan":
        splitter=BULANAN
        format=FORMAT_BULANAN
    elif interval=="harian":
        splitter=HARIAN
        format=FORMAT_HARIAN

    start_s = start[splitter[0]:splitter[1]]
    print(start_s)
    end_s = end[splitter[0]:splitter[1]]
    print(end_s)

    rekap = {}
    list_news = get_all_omed_classified() # mengambil semua berita di solr
    for news in list_news:
        if news['kategori'][0] == 'Netral':
            continue
        else:
            if level==1:
                kategori = '{}'.format(news['kategori'][0])
                
            elif level==2:
                kategori = '{} - {}'.format(news['kategori'][0], news['kategori'][1])
            elif level==3:
                kategori = '{} - {} - {}'.format(news['kategori'][0], news['kategori'][1], news['kategori'][2])

            date = news['timestamp'][splitter[0]:splitter[1]]

            if kategori in rekap: # sudah ada yg kategorinya itu 
                if date in rekap[kategori]: # sudah ada yang bulannya itu 
                    rekap[kategori][date] += 1
                else: # kategorinya ada, tapi bulan tahunnya belum ada
                    rekap[kategori][date] = 1
            else: # belum ada yang kategorinya itu 
                rekap[kategori] = {}
                rekap[kategori][date] = 1
    
    result = []

    for k,v in rekap.items():
        # print('{} {}'.format(k,v))
        new_dict = {
            'name':k,
            'data':v
        }
        result.append(new_dict)

    # print("halo halo " + str(datetime.strptime(end_s,format) > datetime.strptime(start_s,format)))
    # print((datetime.strptime(end_s,format) - datetime.strptime(start_s,format))
    

    return result

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

        con = urllib2.urlopen(HOST_CLASSIFIER + '/category-name/{}'.format(kat))
        res = eval(con.read())
        kat_name = res['result']

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
