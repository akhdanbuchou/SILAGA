import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import json
import base64
import urllib.request as urllib2
from datetime import datetime
import time
import hashlib
from flask import Flask
from flask import jsonify
from flask import Response
from flask import request
import mysql_rest as mysql
import hbase_rest as hbase
import solr_rest as solr
from flask_cors import CORS, cross_origin

# instantiate flask app
app = Flask(__name__)
cors = CORS(app)

# routing path
@app.route("/allnews")
def viewallNews():
    list_id = solr.get_all_online_media_id()
    all_news = hbase.get_all_online_media(list_id)
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

@app.route("/users")
def getUsers():
    list_users = mysql.get_all_users()
    resp = Response(json.dumps(list_users), status=200, mimetype='application/json')
    return resp

@app.route("/user")
def getUserByUsername():
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
   content = request.get_json()
   id_user = content['idUser']
   mysql.delete_user(id_user)
   return 'success'

@app.route('/createKeyword',methods = ['POST'])
def createKeyword():
   content = request.get_json()
   new_kw = {
       'keyword':content['keyword'],
       'kategori_layer_3':content['kategori3']
       }
   mysql.create_kw(new_kw)
   return 'success'

@app.route('/deleteKeyword',methods = ['POST'])
def deleteKeyword():
   content = request.get_json()
   id_kw = content['idKeyword']
   mysql.delete_kw(id_kw)
   return 'success'

@app.route("/keywords")
def getKeywords():
    list_keywords = mysql.get_all_keywords()
    resp = Response(json.dumps(list_keywords), status=200, mimetype='application/json')
    return resp

@app.route("/validate",methods = ['POST','OPTION'])
def validate():
    content = request.get_json()
    data = {
        'username':content['username'],
        'password':content['password']
        }
    result = mysql.validate(data)
    return result

@app.route('/createUpdateBerita',methods = ['POST'])
def createBerita():
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

if __name__ == '__main__':
    app.run(debug=True)

    

