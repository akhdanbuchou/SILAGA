import mysql_rest as mysql

def classify(data):
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

    # result adalah id dari kategori dengan counter tertinggi 
    result = max(categories, key=lambda k: categories[k])    

    return result
