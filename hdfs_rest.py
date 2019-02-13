from hdfs.client import InsecureClient
import base64

dfsWebURI = 'http://10.32.6.225:50070'
dfsBasePath = '/user/magang/'
dfsPathName = 'telegram/'
client = InsecureClient(dfsWebURI)

def getfile(filename):
    with client.read(dfsBasePath+dfsPathName+filename) as reader:
        content = reader.read()
        #akan memprint base 64 dari foto pada content
        str1 = base64.b64encode(content)
        #with open('picture_out.jpg', 'wb') as f:
        #    f.write(content)
        str2 = str.encode("utf-8")

    return str1
