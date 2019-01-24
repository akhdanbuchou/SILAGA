import atexit
import base64
import hashlib
import json
import time
import urllib.request as urllib2
from datetime import datetime
from xml.etree.ElementTree import fromstring

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin
from xmljson import badgerfish as bf

import classifier_rest as classifier
import hbase_rest as hbase
import mysql_rest as mysql
import solr_rest as solr

# instantiate flask app
app = Flask(__name__)
CORS(app)
UPDATE_INTERVAL = 24 # currently run update every 24 hours

# USER RELATED

@app.route("/users")
def getUsers():
    '''
    mengembalikan data semua user 
    '''
    list_users = mysql.get_all_users()
    resp = Response(json.dumps(list_users), status=200, mimetype='application/json')
    return resp

@app.route("/user")
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
def createUser(): # validasi username sudah ada 
    '''
    menerima data user, menyimpan data tsb di DB MySQL
    '''
    content = request.get_json()
    # to-do
    # encrypt password
    # input validation
    new_user = {
       'nama':content['nama'],
       'role':content['role'],
       'username':content['username'],
       'password':content['password']
       }
    mysql.create_user(new_user)
    return 'success'

@app.route('/updateUser',methods = ['POST'])
def updateUser(): # validasi username sudah ada 
    '''
    mengubah data user di DB 
    '''
    content = request.get_json()
    # to-do
    # encrypt password kalo ganti password
    # input validation
    updated_user = {
       'id':content['id'],
       'nama':content['nama'],
       'role':content['role'],
       'username':content['username']
       }
    mysql.update_user(updated_user)
    return 'success'

@app.route('/deleteUser',methods = ['POST'])
def deleteUser():
    '''
    menghapus data user
    '''
    content = request.get_json()
    id_user = content['idUser']
    mysql.delete_user(id_user)
    return 'success'

# WEWENANG RELATED 

@app.route("/roles")
def getRoles():
    '''
    mengembalikan data semua role 
    '''
    list_role = mysql.get_all_roles()
    resp = Response(json.dumps(list_role), status=200, mimetype='application/json')
    return resp

@app.route("/role")
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
def updateRole():
    '''
    mengubah data wewenang di DB 
    '''
    content = request.get_json()
    updated_roles = content['updated_roles']
    print(type(updated_roles))
    print(updated_roles)
    mysql.update_role(updated_roles)
    return 'success'

# KEYWORD RELATED

@app.route('/createKeyword',methods = ['POST'])
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
    mysql.create_kw(new_kw)
    return 'success'

@app.route('/deleteKeyword',methods = ['POST'])
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
def getKeywords():
    '''
    mengembalikan semua keyword yang ada di DB 
    '''
    list_keywords = mysql.get_all_keywords()
    resp = Response(json.dumps(list_keywords), status=200, mimetype='application/json')
    return resp
    
# KATEGORI RELATED

@app.route("/categories")
def getCategories():
    '''
    mengembalikan semua kategori yang ada di DB 
    '''
    list_cat = mysql.get_all_categories()
    resp = Response(json.dumps(list_cat), status=200, mimetype='application/json')
    return resp

@app.route("/categories3")
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
    print(content)
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

@app.route("/allnews")
def viewallNews():
    # list_id = solr.get_all_online_media_id()
    news = solr.get_all_omed_classified()
    # all_news = hbase.get_all_online_media(list_id)
    resp = Response(json.dumps(news), status=200, mimetype='application/json')
    return resp

@app.route('/createBerita',methods = ['POST']) # perlu diuji lagi 
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
    
    # post to hbase collection : online_media
    # hbase.put_online_media(new_berita) 
    
    # also post to solr collection : omed_classified dengan id yang sama 
    solr.add_or_update_to_omed_classified(new_berita)
    return 'success'

@app.route('/updateBerita',methods = ['POST']) 
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

# TELEGRAM RELATED 

@app.route("/allreports")
def viewallReports():
    report = solr.get_all_telegram_reports()
    resp = Response(json.dumps(report), status=200, mimetype='application/json')
    return resp

# CLASSIFIER RELATED

@app.route("/classifySolr")
def classifySolr():
    '''
    mengambil semua berita dari solr : online_media, mengkategorikan ulang berita tersebut,
    kemudian menyimpan ke solr : omed_classified
    '''
    solr.classify_online_media_and_store_to_omed_classified()
    # resp = Response('success', status=200, mimetype='application/json')
    return "success"

def periodic_update():
    solr.classify_online_media_and_store_to_omed_classified()

###

scheduler = BackgroundScheduler()
scheduler.add_job(func=periodic_update, trigger="interval", seconds=UPDATE_INTERVAL*60*60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)
