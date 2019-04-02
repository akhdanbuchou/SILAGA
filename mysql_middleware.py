import mysql.connector

# QUERY-RELATED

IP = '10.32.6.227'
USER = 'magang'
PASSWORD = 'poc**219'
DATABASE = 'lapor'

# dev 
IP = 'localhost'
USER = 'root'
PASSWORD = '1234'
DATABASE = 'poc219'

def special_query(query):
    '''
    menjalankan query bersangkutan (utk kategori)
    '''
    conn = mysql.connector.connect(host=IP, user=USER, passwd=PASSWORD, database=DATABASE)
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
