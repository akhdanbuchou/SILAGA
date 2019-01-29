import mysql_middleware as mysql
import time
from flask import Flask, Response, jsonify, request
from flask_cors import CORS, cross_origin

IP = '10.32.6.225'
PORT = 18881

#dev
IP = '127.0.0.1'

app = Flask(__name__)
CORS(app)

@app.route("/classify", methods = ['POST'])
@cross_origin()
def classify_to_id():
    '''
    request body : list of string, containing the words that will be classified
    {
        "data":["tertib", "ketertiban", "suap"]
    }
    return : string of id of the classification result 
    {
        "result":1 
    }
    '''
    content = request.get_json()
    data = content['data']
    result = {'result':classify(data)}
    resp_json = jsonify(result)
    return resp_json

@app.route("/category-name/<id_cat>")
@cross_origin()
def category_name(id_cat):
    '''
    path variable : id of the category that want to be named
    return : list of string containing 3 levels of the name 
    {
        "result":["Kejahatan", "Konvensional", "Mengganggu ketertiban"]
    }
    '''
    result = {'result':get_category_name(int(id_cat))}
    resp_json = jsonify(result)
    return resp_json

def classify(data):
    '''
    param: array of string 
    mengembalikan id kategori3 
    '''
    # keywords dari MySQL database 
    kw_cat = mysql.get_keywords_category()
    
    categories = {'0':1} # jika tidak ada keyword yang sesuai, hasil adalah default 0 yakni netral 

    # kumpulin semua kategori yang ada keywordnya menjadi dictionary {'category': counter} dengan counter awal 0 
    for kc in kw_cat:
        cat = kc['kategori_layer_3']
        cats = str(cat)
        if cat not in categories:
            categories[cats] = 0

    print(categories) # awal 

    # iterasi tiap keyword, jika keyword ada dalam data, maka counter untuk category itu bertambah 
    for kc in kw_cat:
        kw = kc['keyword']
        cat = kc['kategori_layer_3']
        if kw in data:
            cats = str(cat)
            categories[cats] = categories[cats] + 1

    print(categories) # akhir

    # cat3 adalah id dari kategori dengan counter tertinggi 
    cat3 = eval(max(categories, key=lambda k: categories[k]))
    return cat3
    
def get_category_name(cat):
    '''
    param:int id category 
    '''
    if cat==0:
        return ['Netral','Netral','Netral']
    else:
        cats = mysql.get_all_categories()
        cat1=''
        cat2=''
        cat3=''
        for c1 in cats:
            for c2 in c1['subkategori2']:
                for c3 in c2['subkategori3']:
                    if c3['id']==cat:
                        cat1=c1['kategori1'].capitalize()
                        cat2=c2['kategori2'].capitalize()
                        cat3=c3['kategori3'].capitalize()
        return [cat1,cat2,cat3]

if __name__ == '__main__':
    app.run(debug=True, host=IP, port=PORT)