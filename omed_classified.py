import requests
import json
import urllib.request as urllib2

def add_or_update_to_omed_classified(data):
    headers = {
        'Content-Type': 'application/json',
    }

    json_data = {
        "judul":data['judul'],
        "kategori1":data['kategori1'],
        "kategori2":data['kategori2'],
        "kategori3":data['kategori3'],
        "lokasi":data['lokasi'],
        "tanggal":data['tanggal'],
        "isi":data['isi']
        }
    data = json.dumps(json_data)
    response = requests.post('http://localhost:3333/solr/omed_classified/update/json/docs', headers=headers, data=data)
    print(response)

def delete_from_omed_classified(id_berita):
    headers = {
        'Content-Type': 'text/xml',
    }

    params = (
        ('commit', 'true'),
    )
    
    data = '<delete><id>'+id_berita+'</id></delete>'
    response = requests.post('http://localhost:3333/solr/omed_classified/update', headers=headers, params=params, data=data)
    print(response)

def get_from_omed_classified(id_berita):
    connection = urllib2.urlopen('http://localhost:3333/solr/omed_classified/select?q=id:'+id_berita+'&wt=python')
    response = eval(connection.read())
    print(str(response['response']['numFound'] )+ " documents found.")
    for doc in response['response']['docs']:
        print(doc)
    
get_from_omed_classified("8ce2522d-067e-4128-8991-3429c73ab0a2")
