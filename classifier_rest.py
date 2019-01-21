import mysql_rest as mysql
from time import sleep

def classify(data):
    '''
    mengembalikan array kategori hasil klasifikasi [layer 1, layer 2, layer 3]
    param: array of string 
    '''
    # keywords dari MySQL database 
    kw_cat = mysql.get_keywords_category()
    
    categories = {'0':1} # jika tidak ada keyword yang sesuai, hasil adalah default [0,0,0] yakni netral 

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
        return ['netral','netral','netral']
    else:
        cats = mysql.get_all_categories()
        cat1=''
        cat2=''
        cat3=''
        for c1 in cats:
            for c2 in c1['subkategori2']:
                for c3 in c2['subkategori3']:
                    if c3['id']==cat:
                        cat1=c1['kategori1']
                        cat2=c2['kategori2']
                        cat3=c3['kategori3']
        return [cat1,cat2,cat3]
    

def classify_omed_periodically():
    # iterate all row in solr : online_media and get all the id's and keywords
    
        print("classify")
        # while in that, classify it with classify()

        # save the results in solr : omed_classified 
    
 