import mysql_middleware as mysql
import time

def classify(data):
    '''
    mengembalikan id kategori3 
    param: array of string 
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

    # print(categories) # awal 

    # iterasi tiap keyword, jika keyword ada dalam data, maka counter untuk category itu bertambah 
    for kc in kw_cat:
        kw = kc['keyword']
        cat = kc['kategori_layer_3']
        if kw in data:
            cats = str(cat)
            categories[cats] = categories[cats] + 1

    # print(categories) # akhir

    # cat3 adalah id dari kategori dengan counter tertinggi 
    cat3 = eval(max(categories, key=lambda k: categories[k]))
    print(cat3)
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
    