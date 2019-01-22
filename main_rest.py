import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import json
import base64
import urllib.request as urllib2
from datetime import datetime
import time
import atexit
import hashlib
from flask import Flask
from flask import jsonify
from flask import Response
from flask import request
import mysql_rest as mysql
import hbase_rest as hbase
import solr_rest as solr
import classifier_rest as classifier 
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler

# instantiate flask app
app = Flask(__name__)
cors = CORS(app)
UPDATE_INTERVAL = 24 # interval update

# routing paths
@app.route("/allnews")
def viewallNews():
    # list_id = solr.get_all_online_media_id()
    list_id = solr.get_all_omed_classified()
    start = time.time()
    all_news = hbase.get_all_online_media(list_id)
    end = time.time()
    print(end-start)
    resp = Response(json.dumps(all_news), status=200, mimetype='application/json')
    return resp

@app.route("/news")
def getNewsById():
    id_news = request.args.get('id')
    found_news = {}
    list_id = solr.get_all_online_media_id()
    all_news = hbase.get_all_online_media(list_id)
    for news in all_news:
        if news['id'] == id_news:
            found_news = news
    resp = Response(json.dumps(found_news), status=200, mimetype='application/json')
    return resp

@app.route("/classify")
def classify():
    '''
    menerima array, mengembalikan array string hasil karegori [kategori1, kategori2, kategori3]
    '''
    content = request.get_json()
    arr = content['array']
    category = classifier.classify(arr)
    return category

@app.route("/classifySolr")
def classifySolr():
    '''
    mengambil semua berita dari solr : online_media, mengkategorikan ulang berita tersebut,
    kemudian menyimpan ke solr : omed_classified
    '''
    solr.classify_online_media_and_store_to_omed_classified()
    # resp = Response('success', status=200, mimetype='application/json')
    return "success"

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
def createUser():
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
def updateUser():
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
       'username':content['username'],
       'password':content['password']
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

@app.route("/validate",methods = ['POST','OPTION'])
def validate():
    '''
    param : username dan password
    mengembalikan boolean apakah password tersebut cocok dengan username di DB 
    cek menggunakan BCrypt, sehingga programmer tidak tahu password asli dari user 
    '''
    content = request.get_json()
    data = {
        'username':content['username'],
        'password':content['password']
        }
    result = mysql.validate(data)
    return result

@app.route('/createUpdateBerita',methods = ['POST']) # perlu diuji lagi 
def createBerita():
    '''
    param : json berita seperti di bawah 
    menyimpan berita tersebut di solr : omed_classified dan hbase : online_media
    '''
    content = request.get_json()
    new_berita = {
       "author":"None", # belum ada di form
       "title":content['title'],
       "language":"id", 
       "content":content["content"],
       "url":content['url'], # belum ada di form 
       "sitename":content['sitename'], # belum ada di form 
       "kategori1":content['kategori1'],
       "kategori2":content["kategori2"],
       "kategori3":content["kategori3"],
       "lokasi":content["lokasi"],
       "tanggal":content["tanggal"]
       }
    # menentukan id dari berita untuk di solr : omed_classified dan hbase : online_media
    id_news = hashlib.md5(new_berita['url'].encode()).hexdigest() # id berita didapat dari md5 dari url berita 
    new_berita['id'] = id_news
    
    # post to hbase collection : online_media
    hbase.put_online_media(new_berita)
    
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

# periodical method for periodically update the solr : omed_classified
def periodic_update():
    solr.classify_online_media_and_store_to_omed_classified()

scheduler = BackgroundScheduler()
scheduler.add_job(func=periodic_update, trigger="interval", seconds=UPDATE_INTERVAL*60*60)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True)

    

