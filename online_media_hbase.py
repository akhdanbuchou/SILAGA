import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import json
import base64
import urllib.request as urllib2
from datetime import datetime
import time
from flask import Flask
from flask import jsonify
from flask import Response
from flask import request
import mysql_rest as mysql

# mendapatkan id berita dari solr 
app = Flask(__name__)
ROW_NUM = 3000

connection = urllib2.urlopen('http://localhost:3333/solr/online_media/select?indent=on&q=*:*&rows=' + str(ROW_NUM) + '&wt=python')
response = eval(connection.read())
docs = response['response']['docs']

list_berita = []
loc = []

for doc in docs:    
    try:
        if doc['entity'][0] == 'LOCATION':
            loc.append(doc['value']) 
    except:
        pass
    
    if len(doc['id'].split('_')) < 2:
        
        new_dict = {'id': doc['id'],
                    'loc': loc,
                    'time': doc['timestamp']}
        list_berita.append(new_dict)

        loc = [] #kosongin buat berita selanjutnya 
    

# mengambil semua berita dari hbase berdasarkan id dari solr 

def b64decode(b): # basis 64 decoder
    return base64.b64decode(b)

def bdecode(b): # byte to string decoder 
    return b.decode('utf-8')

headers = {
    'Accept': 'text/xml',
}

list_berita_hbase = []

for berita in list_berita:
    response = requests.get('http://localhost:4444/online_media/' + berita['id'], headers=headers)
    text64 = response.text
    data = bf.data(fromstring(response.text))
    jsondata = json.dumps(data)
    parsed = json.loads(jsondata)

    #list of values
    val = {}
    
    val['id'] = parsed["CellSet"]["Row"]["@key"]
    val['lokasi'] = berita['loc'][0][0]
    val['kategori'] = 'netral'
    val['timestamp'] = berita['time']
    for v in parsed["CellSet"]["Row"]["Cell"]:
        col = b64decode(v['@column'])
        cold = bdecode(col)
        time = v['@timestamp']
        con = b64decode(v['$'])
        cond = bdecode(con)
        
        if "title" in cold:
            val['judul'] = cond
        if "content" in cold:
            val['isi'] = cond
    list_berita_hbase.append(val)


#web service untuk mengambil semua berita yang ada
@app.route("/allnews")
def viewallNews():
    resp = Response(json.dumps(list_berita_hbase), status=200, mimetype='application/json')
    return resp

@app.route("/news")
def getNewsById():
    id_news = request.args.get('id')
    found_news = {}
    for news in list_berita_hbase:
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

@app.route("/validate")
def validate():
    content = request.get_json()
    data = {
        'username':content['username'],
        'password':content['password']
        }
    result = mysql.validate(data)
    resp = Response(json.dumps(result), status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(debug=True)

