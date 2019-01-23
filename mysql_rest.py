import mysql.connector
import security as security

QUERY_USER = ("SELECT * FROM user")

# QUERY-RELATED

def execute_query(query):
    '''
    menjalankan query bersangkutan (utk user)
    '''
    conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    return query + ' executed, connection closed'

def special_query(query):
    '''
    menjalankan query bersangkutan (utk kategori)
    '''
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

# CATEGORY-RELATED 

def get_all_category_3():
    '''
    mengembalikan semua kategori 3 dalam bentuk {'id':<id>, 'kategori': '<kategori1> - <kategori2> - <kategori3>'}
    '''
    QUERY_CAT_1 = ("SELECT * FROM kategori_layer_1")
    QUERY_CAT_2 = ("SELECT * FROM kategori_layer_2")
    QUERY_CAT_3 = ("SELECT * FROM kategori_layer_3")

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

    result = []

    for k3 in kat3list:
        aaa = k3['kategori3']
        for k2 in kat2list:
            if k2['id']==k3['kategori_layer_2']:
                aa = k2['kategori2']
                for k1 in kat1list:
                    if k1['id']==k2['kategori_layer_1']:
                        a = k1['kategori1']
                        id_kat3 = k3['id']
                        kategori = '{} - {} - {}'.format(a.capitalize(), aa.capitalize(), aaa.capitalize())
                        result.append({
                            'id':id_kat3,
                            'kategori':kategori
                        })
    return result

def get_keywords_category():
    '''
    mengembalikan semua keyword dan kategori yang bersangkutan dengan keyword tersebut 
    '''
    QUERY_KEY = ("SELECT * FROM keyword")
    keytup = special_query(QUERY_KEY)
    keylist = []
    for key in keytup:
        k = {'id':key[0],
              'keyword':key[1],
              'kategori_layer_3':key[2]}
        keylist.append(k)
    return keylist

def get_all_categories():
    '''
    mengembalikan semua kategori dengan struktur utuh 
    '''
    QUERY_CAT_1 = ("SELECT * FROM kategori_layer_1")
    QUERY_CAT_2 = ("SELECT * FROM kategori_layer_2")
    QUERY_CAT_3 = ("SELECT * FROM kategori_layer_3")

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

    result = []
    
    for k1 in kat1list:
        subkategori2 = []
        for k2 in kat2list:
            if k2['kategori_layer_1']==k1['id']:
                subkategori3 = []
                for k3 in kat3list:
                    if k3['kategori_layer_2']==k2['id']:      
                        subkategori3.append(k3)
                k2['subkategori3'] = subkategori3
                subkategori2.append(k2)
        k1['subkategori2'] = subkategori2
        result.append(k1)
    return result

# USER-RELATED
    
def get_all_users():
    '''
    mengembalikan data semua user 
    '''
    users = []
    q = QUERY_USER
    conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')
    cur = conn.cursor()
    cur.execute(q)
    result = cur.fetchall()
    for response in result:
        type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in response])
        wewenang = get_nama_wewenang(type_fixed_row[2])
        new_user = {
            'id':type_fixed_row[0],
            'nama':type_fixed_row[1],
            'role':type_fixed_row[2],
            'username':type_fixed_row[3],
            'password':type_fixed_row[4],
            'wewenang':wewenang
            }
        users.append(new_user)
    cur.close()
    conn.close()
    return users
    
def get_user_by_username(uname):
    list_user = get_all_users()
    for user in list_user:
        if user['username']==uname:
            return user

def validate(data):
    '''
    mengembalikan boolean apakah password sesuai dengan username ybs 
    '''
    #find user
    user = get_user_by_username(data['username'])
    if user==None:
        print("False")
        return "False"
    pw = data['password']
    result = str(security.check(pw, user['password']))
    print(result)
    return result

def create_user(data):
    '''
    membuat user baru ke DB 
    '''
    nama = data['nama']
    role = data['role']
    username = data['username']
    password = security.encrypt(data['password'])
    query = ("INSERT INTO user (nama, role, username, password) values(\'{}\',\'{}\',\'{}\',\'{}\')".format(nama, role, username, password))
    execute_query(query)
    
def update_user(data):
    '''
    update user di DB 
    '''
    id_user =  data['id']
    nama = data['nama']
    role = data['role']
    username = data['username']
    password = data['password']
    query = ("UPDATE user SET nama=\'{}\', role=\'{}\', username=\'{}\', password=\'{}\' WHERE id=\'{}\'".format(nama, role, username, password, id_user))
    execute_query(query)

def delete_user(id_user):
    '''
    hapus user dari DB 
    '''
    query = ("DELETE FROM user WHERE id={}".format(id_user))
    execute_query(query)

# WEWENANG RELATED

def get_nama_wewenang(id_role):
    list_role = get_all_roles()
    for role in list_role:
        if role['id']==id_role:
            return role['wewenang']

def get_all_roles():
    roles = []
    q = "SELECT * FROM wewenang"
    conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')
    cur = conn.cursor()
    cur.execute(q)
    result = cur.fetchall()
    for response in result:
        type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in response])
        role = {
            'id':type_fixed_row[0],
            'wewenang':type_fixed_row[1],
            'user_config':str(type_fixed_row[2]),
            'berita_config':str(type_fixed_row[3]),
            'access_report':str(type_fixed_row[4])
        }
        roles.append(role)
    cur.close()
    conn.close()
    return roles

def update_role(roles):
    '''
    mengubah data wewenang 
    '''
    for data in roles:
        id_role = eval(data['id'])
        user_config = eval(data['user_config'])
        berita_config = eval(data['berita_config'])
        access_report = eval(data['access_report'])
        query = ("UPDATE wewenang SET user_config=\'{}\', berita_config=\'{}\', access_report=\'{}\' WHERE id=\'{}\'".format(user_config, berita_config, access_report, id_role))
        execute_query(query)

# KEYWORDS-RELATED

def create_kw(data):
    '''
    buat keyword baru 
    '''
    keyword = data['keyword']
    kategori_layer_3 = data['kategori_layer_3']
    query = ("INSERT INTO keyword (keyword, kategori_layer_3) values(\'{}\',\'{}\')".format(keyword, kategori_layer_3))
    execute_query(query)

def delete_kw(id_kw):
    '''
    hapus keyword 
    '''
    query = ("DELETE FROM keyword WHERE id={}".format(id_kw))
    execute_query(query)

def get_all_keywords():
    '''
    mendapatkan semua keyword dengan struktur utuh 
    '''
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
    return result

