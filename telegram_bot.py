import json
import requests
import time
import base64
import collections
import uuid
import classifier_rest

#utama
#TOKEN = "624146106:AAFCHBOekjG9473XXJJIa2-6ZSjAHezA3L0"
#cadangan
TOKEN  = "687694896:AAHhLbTWalNh-mpuNWWuTqlt0gBUelFB5Fs"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
Sessions = {}
UUID = ""

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    if num_updates > 0:
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        if("text" in updates["result"][last_update]["message"]):
            return ("text", last_update, chat_id)
        else:
            return ("non text",last_update, chat_id)
    else:
        return ("kosong", last_update, 0)


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def save_category_to_solr(id, cat):
    HOST = 'http://localhost:3333/'
    '''
        fungsi insert atau update ke solr collection : telegram
        param type : json
    '''
    data = {}
    # memindakan data dari input web ke data yang akan dimasukkan ke solr : omed_classified
    for k, v in cat.items():
        if k in ['id', 'kategori']:
            data[k] = v
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'id': data['id'],
        'kategori': data['kategori'],
    }
    print(json_data)
    data = json.dumps(json_data)
    response = requests.post(HOST + 'solr/telegram/update/json/docs', headers=headers, data=data)
    print(response)
    print()


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def setUUID(newuuid):
    UUID = newuuid

def getUUID():
    return UUID

def savemessage_to_hbase(line):
    rows = []
    jsonOutput = {"Row": rows}

    baseurl = "http://localhost:8081"

    setUUID(uuid.uuid4())
    rowKey = str(getUUID())
    messagecolumn = "lapor:laporan"

    rowKeyEncoded = stringToBase64(rowKey)
    messagecolumnencoded = stringToBase64(messagecolumn)
    lineencoded = stringToBase64(line)


    cell = collections.OrderedDict([
        ("key", rowKeyEncoded.decode('utf-8')),
        ("Cell",
         [
             {"column": messagecolumnencoded.decode('utf-8'), "$": lineencoded.decode('utf-8')},
         ])
    ])

    rows.append(cell)

    # Submit JSON to REST server
    request = requests.post(baseurl + "/" + 'telegram' + "/" + rowKey, data=json.dumps(jsonOutput), headers={"Content-Type" : "application/json", "Accept" : "application/json",})

def main():
    last_textchat = (None, None, None)
    while True:
        inputan  = get_updates()
        format, intext, chatid = get_last_chat_id_and_text(inputan)
        if (format, intext, chatid) != last_textchat:
            if(chatid in Sessions):
                if (format == "text"):
                    #input text
                    report = inputan["result"][intext]["message"]["text"]
                    if(report.lower() == "selesai"):
                        #savekedatabasekemudianhapus
                        #Hbase.save
                        send_message(Sessions[chatid], chatid)
                        res = ""
                        reportlength = len(Sessions[chatid])
                        words = []
                        for i in range(reportlength):
                            currentword = Sessions[chatid][i].split(" ")
                            for j in currentword:
                                words.append(j)
                            if(i == reportlength - 1 ):
                                res += Sessions[chatid][i]
                            else:
                                res += Sessions[chatid][i] + " "

                        #ini yang disave ke Hbase
                        #Hbase.save(res)
                        savemessage_to_hbase(res)
                        #get kategori kemudian savekesolr
                        category = classifier_rest.classify(words)
                        rescategory = classifier_rest.get_category_name(category)
                        send_message(rescategory, chatid)
                        #solr.save()
                        cat = {
                            'id': getUUID(),
                            'kategori': rescategory,
                        }
                        save_category_to_solr(getUUID(), cat)
                        #cekmessage
                        send_message(res, chatid)

                        Sessions.pop(chatid)
                    else:
                        Sessions[chatid].append(report)
                        #print(report.split(" "))
                        # print(report)
                else:
                    #input nontext
                    #save ke HDFS
                    #HDFS.save
                    print("nontext")
            else:
                if (format == "text"):
                    #input text
                    report = inputan["result"][intext]["message"]["text"]
                    if(report.lower() == "mulai"):
                        #initiate chatid session
                        #save ke dict sessions
                        Sessions[chatid] = []
                    else:
                        #tidak perlu dihandle
                        print('error input')
                else:
                    #input nontext
                    #tidak perlu dihandle
                    print("nontext")

            last_textchat = (format, intext, chatid)
        time.sleep(0.5)


if __name__ == '__main__':
    main()