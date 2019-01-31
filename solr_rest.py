import base64
import json
import time
import urllib.request as urllib2
import urllib
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from xml.etree.ElementTree import fromstring

import requests

import hbase_rest as hbase
import mysql_rest as mysql

ROW_NUM = 10000
HOST = 'http://10.32.6.225:8983/'

#dev
HOST = 'http://localhost:8983/'

ITER_NUM = 5

ALL_KAT_3 = mysql.get_kat_name()
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

    connection = urllib2.urlopen(HOST + 'solr/omed_classified/select?indent=on&q=*:*&rows=' + str(num) + '&wt=python')
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        # print(doc['timestamp'])
        # olah bagian kategori
        kat = doc['kategori'][0]
        katname = None
        if kat == 0:
            kat_name = ['Netral', 'Netral', 'Netral']
        else:
            kat_name = ALL_KAT_3[kat]
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
        name = []
        kat = doc['kategori'][0]
        if kat==0:
            name = ['Netral', 'Netral', 'Netral']
        else:
            lst = ALL_KAT_3[kat]
            name = []
            for i in lst:
                name.append(i.capitalize())


        res['timestamp'] = str(doc['date'][0])[0:10] + " "+str(doc['date'][0])[11:19]
        res['kategori'] = name # override 
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

# CHART RELATED

def get_map(jenis, start, end, keyword):
    dt_start = None
    dt_end = None 
    if start=='-' and end=='-':
        #todo
        dt_end = datetime.now()
        dt_start = dt_end - relativedelta(months=6)
        print(dt_end)
        print(dt_start)
    else:
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_end = datetime.strptime(end, '%Y-%m-%d')

    start = dt_start.strftime('%Y-%m-%dT00:00:00Z')
    end = dt_end.strftime('%Y-%m-%dT00:00:00Z')

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
    test = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows=1&wt=python'.format(HOST, startdate, q)
    print(test)
    connection = urllib2.urlopen(test)
    response = eval(connection.read())
    numfound = response['response']['numFound']
    print(numfound)

    # mengambil data 
    location = []
    url = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, numfound)
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
    dt_start = None
    dt_end = None 
    if start=='-' and end=='-':
        #todo
        dt_end = datetime.now()
        dt_start = dt_end - relativedelta(months=6)
        print(dt_end)
        print(dt_start)
    else:
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_end = datetime.strptime(end, '%Y-%m-%d')
    start = dt_start.strftime('%Y-%m-%dT00:00:00Z')
    end = dt_end.strftime('%Y-%m-%dT00:00:00Z')

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
    test = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows=1&wt=python'.format(HOST, startdate, q)
    print(test)
    connection = urllib2.urlopen(test)
    response = eval(connection.read())
    numfound = response['response']['numFound']
    # print(numfound)

    # mengambil data 
    result = {}
    url = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, numfound)
    print(url)
    connection = urllib2.urlopen(url)
    response = eval(connection.read())
    docs = response['response']['docs']
    for doc in docs:
        kat_id = doc['kategori'][0]
        kat_name = ALL_KAT_3[kat_id][idx].capitalize()

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

def get_rekap(jenis, start, end, keyword, freq):
    
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

    reldelta = None
    if freq=='harian':
        reldelta = relativedelta(days=1)
    elif freq == 'mingguan':
        reldelta = relativedelta(weeks=1)
    elif freq=='bulanan':
        reldelta = relativedelta(months=1)
    elif freq == 'tahunan':
        reldelta = relativedelta(years=1)

    dt_start = None
    dt_end = None 
    if start=='-' and end=='-':
        #todo
        dt_end = datetime.now()
        dt_start = dt_end - relativedelta(months=6)
        print(dt_end)
        print(dt_start)
    else:
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_end = datetime.strptime(end, '%Y-%m-%d')
    
    n_dict = {}
    # dari start, berjalan ke end sesuai interval 
    list_kategori = []
    while dt_start < dt_end:
        # print('sedang di {} '.format(dt_start))
        # sembari di sini, mengambil data di interval ini
        now = dt_start
        nxt = dt_start + reldelta
        now_str = now.strftime('%Y-%m-%dT00:00:00Z')
        nxt_str = nxt.strftime('%Y-%m-%dT00:00:00Z')
        startdate = '[{}%20TO%20{}]'.format(now_str, nxt_str)

        # ambil jumlah row 
        test = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows=1&wt=python'.format(HOST, startdate, q )
        print(test)
        connection = urllib2.urlopen(test)
        response = eval(connection.read())
        numfound = response['response']['numFound']

        # ambill data 
        result = {}
        url = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, numfound)
        print(url)
        connection = urllib2.urlopen(url)
        response = eval(connection.read())
        docs = response['response']['docs']
        
        id_arr = []
        # ambil semua berita di interval tanggal ini , simpan di list id_arr
        d = {}
        for doc in docs:
            # ambil namanya dari kategorinya 
            nama = ALL_KAT_3[doc['kategori'][0]][idx].capitalize()
            
            # memasukkan ke daftar kategori yang ada di interval ini 
            if nama not in list_kategori:
                list_kategori.append(nama)

            # mengupdate jumlah berita dengan kategori tsb 
            if nama not in d:
                d[nama] = 1
            else:
                d[nama] += 1
        
        # masukin id_arr ke arr
        n_dict[now_str[0:10]] = d

        # increment 
        dt_start += reldelta
    
    # beberes
    print(list_kategori)
    axisx = []
    for k in n_dict.keys():
        axisx.append(k)

    result = []
    for k in list_kategori:
        rekap = []

        #jika di interval itu ada yang namanya ini, tambahin, kalo gaada, 0 
        for key, value in n_dict.items():
            if k in value.keys():
                rekap.append(value[k])
            else:
                rekap.append(0)

        #masukin rekap untuk kategori ini ke dict 
        ddddddd = {
            'namaGangguan':k,
            'jumlahPerInterval':rekap
            } 

        #masukin dict ini ke result 
        result.append(ddddddd)

    data = {
        'axisx':axisx,
        'result':result
    }

    return data
