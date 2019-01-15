import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', passwd=None, database='poc219')

cur = conn.cursor()

QUERY_USER = ("SELECT * FROM user")
QUERY_CAT_1 = ("SELECT * FROM kategori_layer_1")
QUERY_CAT_2 = ("SELECT * FROM kategori_layer_2")
QUERY_CAT_3 = ("SELECT * FROM kategori_layer_3")
QUERY_KEY = ("SELECT * FROM keywords")

def run_this_query(query):
    q = query
    cur.execute(q)
    result = cur.fetchall()
    for response in result:
        type_fixed_row = tuple([el.decode('utf-8') if type(el) is bytearray else el for el in response])
        print(str(type_fixed_row[0]) + " " + type_fixed_row[1] + " " + str(type_fixed_row[2]))
    
def get_all_users():
    users = []
    q = QUERY_USER
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
    return users

def get_all_cat_1():
    run_this_query(QUERY_CAT_1)

def get_all_cat_2():
    run_this_query(QUERY_CAT_2)

def get_all_cat_3():
    run_this_query(QUERY_CAT_3)
    
def get_all_key():
    run_this_query(QUERY_KEY)
    



