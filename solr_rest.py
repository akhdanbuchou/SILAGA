import base64
import json
import time
import urllib.request as urllib2
import urllib
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from xml.etree.ElementTree import fromstring
from abc import ABCMeta, abstractmethod
import requests

import hbase_rest as hbase
import mysql_rest as mysql
'''
ROW_NUM = 10000
HOST = 'http://10.32.6.225:8983/'

#dev
'''
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
            kname = ALL_KAT_3[kat]
            kat_name = []
            for k in kname:
                kat_name.append(k.capitalize())
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

def get_telegram_medias(id_tel):
    '''
    mengembalikan json berisi list nama image dan video sebuah report telegram 
    '''
    uri = '{}solr/telegram/select?indent=on&q=id:{}&rows=1&wt=python'.format(HOST, id_tel)
    conn = urllib2.urlopen(uri)
    response = eval(conn.read())
    docs = response['response']['docs']
    list_gambar = []
    list_rekaman = []
    # mencoba mengambil gambar 
    try:
        list_gambar = docs[0]['gambar'][0].split(',')
    except Exception:
        pass
    # mencoba mengambil gambar 
    try:
        list_rekaman = docs[0]['rekaman'][0].split(',')
    except Exception:
        pass
    
    data = {
        "list_gambar":list_gambar,
        "list_rekaman":list_rekaman
    }
    return data

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
    print(docs)
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

    list_kategori = list(ALL_KAT_3.values())
    unique_category = list()

    for category in list_kategori:
        if category[idx].capitalize() not in unique_category:
            unique_category.append(category[idx].capitalize())

    # dari start, berjalan ke end sesuai interval 
    # list_kategori = unique_category
    while dt_start < dt_end:
        d = {el:0 for  el in unique_category}       
        
        # print('sedang di {} '.format(dt_start))
        # sembari di sini, mengambil data di interval ini
        now = dt_start
        nxt = dt_start + reldelta
        now_str = now.strftime('%Y-%m-%dT00:00:00Z')
        nxt_str = nxt.strftime('%Y-%m-%dT00:00:00Z')
        startdate = '[{}%20TO%20{}]'.format(now_str, nxt_str)

        # ambil jumlah row 
        test = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows=1&wt=python'.format(HOST, startdate, q )
        # print(test)
        connection = urllib2.urlopen(test)
        response = eval(connection.read())
        numfound = response['response']['numFound']

        # ambill data 
        result = {}
        url = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, numfound)
        # print(url)
        connection = urllib2.urlopen(url)
        response = eval(connection.read())
        docs = response['response']['docs'] ##docs adalah berita
        
        
        id_arr = []
        # ambil semua berita di interval tanggal ini , simpan di list id_arr
        
        
        for doc in docs:
            # ambil namanya dari kategorinya 
            nama = ALL_KAT_3[doc['kategori'][0]][idx].capitalize()
            
            
            # memasukkan ke daftar kategori yang ada di interval ini
            
            # if nama not in list_kategori:
            #     list_kategori.append(nama)
            # print(list_kategori)

            # mengupdate jumlah berita dengan kategori tsb 
            if nama in d:
                d[nama] += 1
        
        # print(d)
        # masukin id_arr ke arr
        n_dict[now_str[0:10]] = d

        # increment 
        dt_start += reldelta
    
    # beberes
    
    # print(n_dict.items(), "n_dict")
    axisx = []
    for k in n_dict.keys():
        axisx.append(k)

    # print(list_kategori)
    result = []
    for k in unique_category:
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

def detail_rekap(jenis, start, freq):
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

    dt_start = datetime.strptime(start, '%Y-%m-%d')
    dt_end = dt_start + reldelta
    #print('aaaaaaaaaaaaaaaa {} {}'.format(dt_start, dt_end))

    now = dt_start.strftime('%Y-%m-%dT00:00:00Z')
    nxt = dt_end.strftime('%Y-%m-%dT00:00:00Z')

    startdate = '[{}%20TO%20{}]'.format(now, nxt)

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

    for doc in docs:
        kat = doc['kategori'][0]
        katname = None
        if kat == 0:
            kat_name = ['Netral', 'Netral', 'Netral']
        else:
            kname = ALL_KAT_3[kat]
            kat_name = []
            for k in kname:
                kat_name.append(k.capitalize())
        doc['kategori'] = kat_name
        doc['timestamp'] = str(doc['timestamp'])[0:10] + " "+str(doc['timestamp'])[11:19]
        doc['kategori'] = kat_name # override 
        doc['content'] = doc['content'][0]
        doc['title'] = doc['title'][0]

    return docs

def get_rekap_telegram(jenis, start, end, keyword, freq):
    
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

    list_kategori = list(ALL_KAT_3.values())
    unique_category = list()

    for category in list_kategori:
        if category[idx].capitalize() not in unique_category:
            unique_category.append(category[idx].capitalize())

    # dari start, berjalan ke end sesuai interval 
    # list_kategori = unique_category
    while dt_start < dt_end:
        d = {el:0 for  el in unique_category}       
        
        # print('sedang di {} '.format(dt_start))
        # sembari di sini, mengambil data di interval ini
        now = dt_start
        nxt = dt_start + reldelta
        now_str = now.strftime('%Y-%m-%dT00:00:00Z')
        nxt_str = nxt.strftime('%Y-%m-%dT00:00:00Z')
        startdate = '[{}%20TO%20{}]'.format(now_str, nxt_str)

        # ambil jumlah row 
        test = '{}solr/telegram/select?indent=on&q=date:{}%20AND%20{}&rows=1&wt=python'.format(HOST, startdate, q )
        # print(test)
        connection = urllib2.urlopen(test)
        response = eval(connection.read())
        numfound = response['response']['numFound']

        # ambill data 
        result = {}
        url = '{}solr/telegram/select?indent=on&q=date:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, numfound)
        # print(url)
        connection = urllib2.urlopen(url)
        response = eval(connection.read())
        docs = response['response']['docs'] ##docs adalah berita
        
        
        id_arr = []
        # ambil semua berita di interval tanggal ini , simpan di list id_arr
        
        
        for doc in docs:
            # ambil namanya dari kategorinya 
            nama = ALL_KAT_3[doc['kategori'][0]][idx].capitalize()
            
            
            # memasukkan ke daftar kategori yang ada di interval ini
            
            # if nama not in list_kategori:
            #     list_kategori.append(nama)
            # print(list_kategori)

            # mengupdate jumlah berita dengan kategori tsb 
            if nama in d:
                d[nama] += 1
        
        # print(d)
        # masukin id_arr ke arr
        n_dict[now_str[0:10]] = d

        # increment 
        dt_start += reldelta
    
    # beberes
    
    # print(n_dict.items(), "n_dict")
    axisx = []
    for k in n_dict.keys():
        axisx.append(k)

    # print(list_kategori)
    result = []
    for k in unique_category:
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

def get_pie_telegram(jenis, start, end, keyword): 
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
    test = '{}solr/telegram/select?indent=on&q=date:{}%20AND%20{}&rows=1&wt=python'.format(HOST, startdate, q)
    print(test)
    connection = urllib2.urlopen(test)
    response = eval(connection.read())
    numfound = response['response']['numFound']
    # print(numfound)

    # mengambil data 
    result = {}
    url = '{}solr/telegram/select?indent=on&q=date:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, numfound)
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

    '''
date:[2018-12-01T07:03:17Z TO 2019-02-01T07:03:17Z]
    '''

class SolrAccessor:

    def __init__(self):
        pass

    def get_query_category_and_index(cls, jenis, idx=1):
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
        
        return q, idx

    def get_query_frequency(self, freq, reldelta=None):
        if freq =='harian':
            reldelta = relativedelta(days=1)
        elif freq == 'mingguan':
            reldelta = relativedelta(weeks=1)
        elif freq=='bulanan':
            reldelta = relativedelta(months=1)
        elif freq == 'tahunan':
            reldelta = relativedelta(years=1)
        
        return reldelta

    def get_query_timespan(self, start, end):
        if start=='-' and end=='-':
            dt_end = datetime.now()
            dt_start = dt_end - relativedelta(months=6)
        else:
            dt_start = datetime.strptime(start, '%Y-%m-%d')
            dt_end = datetime.strptime(end, '%Y-%m-%d')

        return dt_start, dt_end
    
    def get_query_time_converted(self, now, nxt):
        now_str = now.strftime('%Y-%m-%dT00:00:00Z')
        nxt_str = nxt.strftime('%Y-%m-%dT00:00:00Z')
        return '[{}%20TO%20{}]'.format(now_str, nxt_str)

    @abstractmethod
    def request_solr_entry(self, host, startdate, q, rows=1000):
        return

    def get_category_list(self, all_category, idx, jenis):
        list_kategori = all_category
        unique_category = list()
        common_category = list()

        for category in list_kategori:
            if category[0].capitalize() not in common_category:
                common_category.append(category[0].capitalize())

        if idx != 0:
            sought_category = common_category[int(jenis)-1]
            for category in list_kategori:
                if category[0].capitalize() == sought_category and category[1].capitalize() not in unique_category:
                    unique_category.append(category[1].capitalize())
            
        else:
            unique_category = common_category

        return unique_category

    def get_recap(self, jenis, start, end, keyword, freq):
        q, idx = self.get_query_category_and_index(jenis)    
        reldelta = self.get_query_frequency(freq)
        dt_start, dt_end = self.get_query_timespan(start,end)
        
        n_dict = {}

        '''
        list_kategori = list(ALL_KAT_3.values())
        unique_category = list()
        common_category = list()

        for category in list_kategori:
            if category[0].capitalize() not in common_category:
                common_category.append(category[0].capitalize())

        if idx != 0:
            sought_category = common_category[int(jenis)-1]
            for category in list_kategori:
                if category[0].capitalize() == sought_category and category[1].capitalize() not in unique_category:
                    unique_category.append(category[1].capitalize())
            
        else:
            unique_category = common_category
        '''

        unique_category = self.get_category_list(list(ALL_KAT_3.values()), idx, jenis)

        # print(unique_category)
        # dari start, berjalan ke end sesuai interval 
        while dt_start < dt_end:
            d = {el:0 for  el in unique_category}       

            # sembari di sini, mengambil data di interval ini
            now = dt_start
            nxt = dt_start + reldelta
        
            startdate = self.get_query_time_converted(now,nxt)
            response = self.request_solr_entry(HOST, startdate, q)
            try:
                docs = response['response']['docs'] ##docs adalah berita
            except:
                docs = list()
            
            
            id_arr = []
            # ambil semua berita di interval tanggal ini , simpan di list id_arr
            
            
            for doc in docs:
                # ambil namanya dari kategorinya 
                nama = ALL_KAT_3[doc['kategori'][0]][idx].capitalize()
                # print("nama ", nama)
                # mengupdate jumlah berita dengan kategori tsb 
                if nama in d:
                    d[nama] += 1
            
            # masukin id_arr ke arr
            now_str = now.strftime('%Y-%m-%dT00:00:00Z')
            n_dict[now_str[0:10]] = d
            dt_start += reldelta

        ##finalize
        axisx = []
        for k in n_dict.keys():
            axisx.append(k)

        # print(list_kategori)
        result = []
        for k in unique_category:
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

    def get_pie(self, jenis, start, end, keyword): 

        dt_start, dt_end = self.get_query_timespan(start,end)
        startdate = self.get_query_time_converted(dt_start,dt_end)
        q, idx = self.get_query_category_and_index(jenis)

        response = self.request_solr_entry(HOST, startdate, q)
        docs = response['response']['docs']

        unique_category = self.get_category_list(list(ALL_KAT_3.values()), idx, jenis)

        result = {el:0 for  el in unique_category} 
        for doc in docs:
            kat_id = doc['kategori'][0]
            kat_name = ALL_KAT_3[kat_id][idx].capitalize()

            if kat_name in result:
                result[kat_name] += 1
        
        arr = list()
        for k,v in result.items():
            new_dict = {}
            new_dict['namaGangguan'] = k
            new_dict['jumlahGangguan'] = v
            arr.append(new_dict)
        return arr

    def get_map(self, jenis, start, end, keyword):

        dt_start, dt_end = self.get_query_timespan(start,end)
        startdate = self.get_query_time_converted(dt_start,dt_end)
        q, idx = self.get_query_category_and_index(jenis)
 
        response = self.request_solr_entry(HOST, startdate, q)
        docs = response['response']['docs']

        # mengambil data 
        location = []
        for doc in docs:
            lokasi = doc['lokasi']
            for tempat in lokasi:
                if tempat.capitalize() not in location:
                    location.append(tempat.capitalize())

        return location


class Solr_Accessor_Omed_Classified(SolrAccessor):
    
    def __init__(self):
        super().__init__()

    def request_solr_entry(self, host, startdate, q, rows=1000):
        query = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, rows)
        print(query)
        try:
            connection = urllib2.urlopen(query)
            return eval(connection.read())

            if response['response']['numFound'] > rows:
                query = '{}solr/omed_classified/select?indent=on&q=timestamp:{}%20AND%20{}&rows={}&wt=python'.format(
                    HOST, startdate, q, response['response']['numFound']
                    )
                connection = urllib2.urlopen(query)
                response =  eval(connection.read())
            
            return response
        except:
            return dict()
        
    def detail_rekap(self, jenis, start, freq):
        reldelta = self.get_query_frequency(freq)
        dt_start, dt_end = self.get_query_timespan(start,start)
        dt_end = dt_start + reldelta
        startdate = self.get_query_time_converted(dt_start,dt_end)
        q, idx = self.get_query_category_and_index(jenis)

        response = self.request_solr_entry(HOST, startdate, q)

        docs = response['response']['docs']

        # ambill data 
        result = {}

        for doc in docs:
            kat = doc['kategori'][0]
            katname = None
            if kat == 0:
                kat_name = ['Netral', 'Netral', 'Netral']
            else:
                kname = ALL_KAT_3[kat]
                kat_name = []
                for k in kname:
                    kat_name.append(k.capitalize())
            doc['kategori'] = kat_name
            print("")
            doc['timestamp'] = str(doc['timestamp'])[0:10] + " "+str(doc['timestamp'])[11:19]
            doc['kategori'] = kat_name # override 
            doc['content'] = doc['content'][0]
            doc['title'] = doc['title'][0]

        return docs

class Solr_Accessor_Telegram(SolrAccessor):

    def __init__(self):
        super().__init__()

    def request_solr_entry(self, host, startdate, q, rows=100):
        query = '{}solr/telegram/select?indent=on&q=date:{}%20AND%20{}&rows={}&wt=python'.format(HOST, startdate, q, rows)
        try:
            connection = urllib2.urlopen(query)
            response =  eval(connection.read())

            if response['response']['numFound'] > rows:
                query = '{}solr/telegram/select?indent=on&q=date:{}%20AND%20{}&rows={}&wt=python'.format(
                    HOST, startdate, q, response['response']['numFound']
                    )
                connection = urllib2.urlopen(query)
                response =  eval(connection.read())
            
            return response
        except:
            return dict()

    def detail_rekap(self, jenis, start, freq):
        reldelta = self.get_query_frequency(freq)
        dt_start, dt_end = self.get_query_timespan(start,start)
        dt_end = dt_start + reldelta
        startdate = self.get_query_time_converted(dt_start,dt_end)
        q, idx = self.get_query_category_and_index(jenis)

        response = self.request_solr_entry(HOST, startdate, q)
   
        docs = response['response']['docs']

        # ambill data 
        result = {}

        for doc in docs:
            kat = doc['kategori'][0]
            katname = None
            if kat == 0:
                kat_name = ['Netral', 'Netral', 'Netral']
            else:
                kname = ALL_KAT_3[kat]
                kat_name = []
                for k in kname:
                    kat_name.append(k.capitalize())
            doc['kategori'] = kat_name
            doc['date'] = str(doc['date'])[2:12] + " "+str(doc['date'])[13:21]
            doc['kategori'] = kat_name # override 

            try:
                doc['gambar'] = doc['gambar']
            except:
                doc['gambar'] = []
            
        return docs

    def get_map(*args):
        pass
        