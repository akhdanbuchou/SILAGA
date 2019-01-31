import atexit
import base64
import hashlib
import json
import time
import urllib.request as urllib2
from datetime import datetime
from xml.etree.ElementTree import fromstring

import requests
from flask import Flask, Response, jsonify, request, send_file

import hbase_rest as hbase
import mysql_rest as mysql
import solr_rest as solr
import printer as printer

from flask_cors import CORS, cross_origin

# instantiate flask app
app = Flask(__name__,static_folder='docx')
CORS(app)

IP = '10.32.6.225'
PORT = 18880
# dev 
IP = '127.0.0.1'
PORT = 5000

# LAPORAN RELATED
@app.route('/cetak', methods=['POST'])
@cross_origin()
def download():
    content = request.get_json()
    piedata = content['piedata']
    linedata = content['linedata']
    printer.createLaporan(pie_data, line_data)
    return send_file('lapor.docx')

# USER RELATED

@app.route("/users")
@cross_origin()
def getUsers():
    '''
    mengembalikan data semua user 
    '''
    list_users = mysql.get_all_users()
    resp = Response(json.dumps(list_users), status=200, mimetype='application/json')
    return resp

@app.route("/user")
@cross_origin()
def getUserByUsername():
    '''
    menerima username, mengembalikan data user dengan username tersebut 
    '''
    username = request.args.get('username')
    list_users = mysql.get_all_users()
    found_user = {}
    for user in list_users:
        if user['username'] == username:
            found_user = user
    resp = Response(json.dumps(found_user), status=200, mimetype='application/json')
    return resp

@app.route('/createUser',methods = ['POST'])
@cross_origin()
def createUser():  
    '''
    menerima data user, menyimpan data tsb di DB MySQL
    '''
    list_users = mysql.get_all_users()
    exists = False 
    content = request.get_json()
    for user in list_users: 
        if user['username']==content['username']:
            exists = True
    if exists:
        return 'False'
    else:
        new_user = {
        'nama':content['nama'],
        'role':content['role'],
        'username':content['username'],
        'password':content['password']
        }
        mysql.create_user(new_user)
        return 'True'

@app.route('/updateUser',methods = ['POST'])
@cross_origin()
def updateUser(): # validasi username sudah ada , bug kalau role gak diubah
    '''
    mengubah data user di DB 
    '''
    content = request.get_json()
    updated_user = {
       'id':content['id'],
       'nama':content['nama'],
       'role':content['role'],
       'username':content['username']
       }
    mysql.update_user(updated_user)
    return 'success'

@app.route('/deleteUser',methods = ['POST'])
@cross_origin()
def deleteUser():
    '''
    menghapus data user
    '''
    content = request.get_json()
    id_user = content['idUser']
    mysql.delete_user(id_user)
    return 'success'

# ROLE RELATED 

@app.route("/roles")
@cross_origin()
def getRoles():
    '''
    mengembalikan data semua role 
    '''
    list_role = mysql.get_all_roles()
    resp = Response(json.dumps(list_role), status=200, mimetype='application/json')
    return resp

@app.route("/role")
@cross_origin()
def getRoleById():
    '''
    mengembalikan data role dengan id berikut 
    '''
    id_role = eval(request.args.get('id'))
    list_role = mysql.get_all_roles()
    found_role = {}
    for role in list_role:
        if role['id']==(id_role):
            found_role = role
    resp = Response(json.dumps(found_role), status=200, mimetype='application/json')
    return resp

@app.route('/updateRole',methods = ['POST'])
@cross_origin()
def updateRole():
    '''
    mengubah data wewenang di DB 
    '''
    content = request.get_json()
    updated_roles = content['updated_roles']
    # print(updated_roles)
    mysql.update_role(updated_roles)
    return 'success'

# KEYWORD RELATED

@app.route("/keywords-by-category/<kategori>")
@cross_origin()
def getKeywordsByKategori(kategori):
    '''
    mengembalikan semua keyword yang kategorinya <kategori>
    '''
    list_keywords = mysql.get_keywords_by_category(kategori)
    resp = Response(json.dumps(list_keywords), status=200, mimetype='application/json')
    return resp

@app.route('/createKeyword',methods = ['POST'])
@cross_origin()
def createKeyword():
    '''
    membuat keyword baru 
    param {keywords, id dari kategori3}
    '''
    content = request.get_json()
    new_kw = {
       'keyword':content['keyword'],
       'kategori_layer_3':content['kategori3']
       }
    kw = mysql.create_kw(new_kw)
    return str(kw)

@app.route('/deleteKeyword',methods = ['POST'])
@cross_origin()
def deleteKeyword():
    '''
    param : id 
    menghapus keyword dengan id tersebut 
    '''
    content = request.get_json()
    id_kw = content['idKeyword']
    mysql.delete_kw(id_kw)
    return 'success'

@app.route("/keywords")
@cross_origin()
def getKeywords():
    '''
    mengembalikan semua keyword yang ada di DB 
    '''
    list_keywords = mysql.get_all_keywords()
    resp = Response(json.dumps(list_keywords), status=200, mimetype='application/json')
    return resp
    
# KATEGORI RELATED

@app.route("/categories")
@cross_origin()
def getCategories():
    '''
    mengembalikan semua kategori yang ada di DB 
    '''
    list_cat = mysql.get_all_categories()
    resp = Response(json.dumps(list_cat), status=200, mimetype='application/json')
    return resp

@app.route("/categories3")
@cross_origin()
def getCategories3():
    '''
    mengembalikan semua kategori 3 yang ada di DB
    '''
    list_cat_3 = mysql.get_all_category_3()
    resp = Response(json.dumps(list_cat_3), status=200, mimetype='application/json')
    return resp

# VALIDASI RELATED

@app.route("/validate", methods = ['POST','OPTIONS'])
@cross_origin()
def validate():
    '''
    param : json {username dan password}
    mengembalikan boolean apakah password tersebut cocok dengan username di DB 
    cek menggunakan BCrypt, sehingga programmer tidak tahu password asli dari user 
    '''
    content = request.get_json()
    user = {}
    data = {
        'username':content['username'],
        'password':content['password']
        }
    valid = mysql.validate(data)
    if valid!=None: # user exists and password is correct 
        user = mysql.get_user_by_username(content['username'])

    result = {
        "valid":valid,
        "user":user
    }
    resp_json = jsonify(result)
    return resp_json

# BERITA RELATED

@app.route("/allnews/<jumlah>")
@cross_origin()
def viewallNews(jumlah):
    s = time.time()
    news = solr.get_all_omed_classified(jumlah) # mengambil berita di solr : omed_classified sejumlah <jumlah>
    e = time.time()
    print(e-s)
    resp = Response(json.dumps(news), status=200, mimetype='application/json') # solr
    return resp

@app.route('/createBerita',methods = ['POST']) # perlu diuji lagi 
@cross_origin()
def createBerita():
    '''
    param : json berita seperti di bawah 
    menyimpan berita tersebut di solr : omed_classified dan hbase : online_media
    '''
    content = request.get_json()
    new_berita = {
       "author":content['author'], # belum ada di form
       "title":content['title'],
       "language":content['language'], 
       "content":content["content"],
       "url":content['url'],
       "timestamp":content['timestamp'],
       "sitename":content['sitename'], 
       "kategori":content["kategori"],
       "lokasi":content["lokasi"]
       }
    # menentukan id dari berita untuk di solr : omed_classified dan hbase : online_media
    id_news = hashlib.md5(new_berita['url'].encode()).hexdigest() # id berita didapat dari md5 dari url berita 
    new_berita['id'] = id_news
    
    # also post to solr collection : omed_classified dengan id yang sama 
    solr.add_or_update_to_omed_classified(new_berita)
    return 'success'

@app.route('/updateBerita',methods = ['POST']) 
@cross_origin()
def updateBerita():
    '''
    param : json berita seperti di bawah 
    menyimpan berita tersebut di solr : omed_classified dan hbase : online_media
    '''
    content = request.get_json()
    new_berita = {
        "id":content['id'],
        "author":content['author'], # belum ada di form
        "title":content['title'],
        "language":content['language'], 
        "content":content["content"],
        "url":content['url'],
        "timestamp":content['timestamp'],
        "sitename":content['sitename'], 
        "kategori":content["kategori"],
        "lokasi":content["lokasi"]
       }
    
    # post to hbase collection : online_media
    # hbase.put_online_media(new_berita) 
    
    # also post to solr collection : omed_classified dengan id yang sama 
    solr.add_or_update_to_omed_classified(new_berita)
    return 'success'

@app.route('/deleteNews',methods = ['POST'])
@cross_origin()
def delete_news():
    '''
    menghapus berita dari hbase : online_media dan solr : omed_classified
    '''
    content = request.get_json()
    id_news = content['id']

    # delete from hbase online_media
    hbase.delete_a_news(id_news)

    # delete from solr omed_classified
    solr.delete_from_omed_classified(id_news)
    return 'success'

@app.route("/rekap/<jenis>/<start>/<end>/<keyword>/<freq>")
@cross_origin()
def rekapBerita(jenis, start, end, keyword, freq):

    result = solr.get_rekap(jenis, start, end, keyword, freq)

    resp = Response(json.dumps(result), status=200, mimetype='application/json') 
    return resp

# CHART RELATED

@app.route("/pie-chart/<jenis>/<start>/<end>/<keyword>")
@cross_origin()
def pieChart(jenis, start, end, keyword):
    result = solr.get_pie(jenis, start, end, keyword)

    resp = Response(json.dumps(result), status=200, mimetype='application/json') 
    return resp

@app.route("/map/<jenis>/<start>/<end>/<keyword>")
@cross_origin()
def map(jenis, start, end, keyword):
    result = solr.get_map(jenis, start, end, keyword)
    resp = Response(json.dumps(result), status=200, mimetype='application/json') 
    return resp

# TELEGRAM RELATED 

@app.route("/allreports")
@cross_origin()
def viewallReports():
    report = solr.get_all_telegram_reports()
    resp = Response(json.dumps(report), status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=True, port=PORT, host=IP)
