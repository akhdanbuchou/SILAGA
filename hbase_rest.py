import base64
import hashlib
import json
import time
import urllib.request as urllib2
from datetime import datetime
from xml.etree.ElementTree import fromstring

import requests
from xmljson import badgerfish as bf

import mysql_middleware as mysql

URL = 'http://10.32.6.225:16001'
###
# development
URL = 'http://localhost:16001'
###

def b64decode(b): # basis 64 decoder
    return base64.b64decode(b)

def bdecode(b): # byte to string decoder 
    return b.decode('utf-8')

def bungkus(s):
    '''
    param : string 
    encode byte -> encode 64 -> decode string 
    '''
    return bdecode(b64encode(sencode(s)))

def sencode(s):
    return s.encode()

def b64encode(b):
    return base64.b64encode(b)

def get_isi_news(id_news):
    '''
    mengembalikan isi suatu berita dengan id tersebut
    '''
    headers = {
        'Accept': 'application/json',
    }
    response = requests.get(URL + '/online_media/' + id_news, headers=headers)
    text64 = response.text
    data = json.loads(text64)
    #list of values
    result = ""
    cells = data['Row'][0]['Cell']
    for v in cells:
        col = b64decode(v['column'])
        cold = bdecode(col)
        con = b64decode(v['$'])
        cond = bdecode(con)
        if "content" in cold:
            result = cond
    return result
