import mysql.connector
import security as security

QUERY_USER = ("SELECT * FROM user")

def execute_query(query):
    print(query)
    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    finally:
        cur.close()
        conn.close()
        return query + ' executed, connection closed'

def special_query(query):
    print(query)
    conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchall()
    res = []
    for response in result:
        type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in response])
        res.append(type_fixed_row)
        #print(type_fixed_row)
    cur.close()
    conn.close()
    return res
   
def get_all_keywords():
    QUERY_CAT_1 = ("SELECT * FROM kategori_layer_1")
    QUERY_CAT_2 = ("SELECT * FROM kategori_layer_2")
    QUERY_CAT_3 = ("SELECT * FROM kategori_layer_3")
    QUERY_KEY = ("SELECT * FROM keyword")

    kat1tup = special_query(QUERY_CAT_1)
    kat1list = []
    for tup in kat1tup:
        k1 = {'id':tup[0],
              'kategori1':tup[1]}
        kat1list.append(k1)

    kat2tup = special_query(QUERY_CAT_2)
    kat2list = []
    for tup in kat2tup:
        k2 = {'id':tup[0],
              'kategori2':tup[1],
              'kategori_layer_1':tup[2]}
        kat2list.append(k2)
    
    kat3tup = special_query(QUERY_CAT_3)
    kat3list = []
    for tup in kat3tup:
        k3 = {'id':tup[0],
              'kategori3':tup[1],
              'kategori_layer_2':tup[2]}
        kat3list.append(k3)

    keytup = special_query(QUERY_KEY)
    keylist = []
    for key in keytup:
        k = {'id':key[0],
              'keyword':key[1],
              'kategori_layer_3':key[2]}
        keylist.append(k)

    result = []
    
    for k1 in kat1list:
        subkategori2 = []
        for k2 in kat2list:
            if k2['kategori_layer_1']==k1['id']:
                subkategori3 = []
                for k3 in kat3list:
                    if k3['kategori_layer_2']==k2['id']:
                        listKeyword = []
                        for key in keylist:
                            if key['kategori_layer_3']==k3['id']:
                                listKeyword.append(key)
                        k3['keyword'] = listKeyword       
                        subkategori3.append(k3)
                k2['subkategori3'] = subkategori3
                subkategori2.append(k2)
        k1['subkategori2'] = subkategori2
        result.append(k1)
    '''
    for k1 in result:
        print(">" + k1['kategori1'])
        for k2 in k1['subkategori2']:
            print(" >" + k2['kategori2'])
            for k3 in k2['subkategori3']:
                print("  >" + k3['kategori3'])
                for key in k3['keyword']:
                    print("   >" + key['keyword'])
    '''
    return result
    
def get_all_users():
    users = []
    q = QUERY_USER
    try:
        conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')
        cur = conn.cursor()
        cur.execute(q)
        result = cur.fetchall()
        for response in result:
            type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in response])
            new_user = {
                'id':type_fixed_row[0],
                'nama':type_fixed_row[1],
                'role':type_fixed_row[2],
                'username':type_fixed_row[3],
                'password':type_fixed_row[4]}
            users.append(new_user)
    finally:
        cur.close()
        conn.close()
        return users
    
def get_user_by_username(uname):
    list_user = get_all_users()
    for user in list_user:
        if user['username']==uname:
            return user

def validate(data):
    #find user
    user = get_user_by_username(data['username'])
    pw = data['password']
    result = str(security.check(pw, user['password']))
    print(result)
    return result

def create_user(data):
    nama = data['nama']
    role = data['role']
    username = data['username']
    password = security.encrypt(data['password'])
    query = ("INSERT INTO user (nama, role, username, password) values(\'{}\',\'{}\',\'{}\',\'{}\')".format(nama, role, username, password))
    execute_query(query)
    
def update_user(data):
    id_user =  data['id']
    nama = data['nama']
    role = data['role']
    username = data['username']
    password = data['password']
    query = ("UPDATE user SET nama=\'{}\', role=\'{}\', username=\'{}\', password=\'{}\' WHERE id=\'{}\'".format(nama, role, username, password, id_user))
    execute_query(query)

def delete_user(id_user):
    query = ("DELETE FROM user WHERE id={}".format(id_user))
    execute_query(query)

def create_kw(data):
    keyword = data['keyword']
    kategori_layer_3 = data['kategori_layer_3']
    query = ("INSERT INTO keyword (keyword, kategori_layer_3) values(\'{}\',\'{}\')".format(keyword, kategori_layer_3))
    execute_query(query)

def delete_kw(id_kw):
    query = ("DELETE FROM keyword WHERE id={}".format(id_kw))
    execute_query(query)



