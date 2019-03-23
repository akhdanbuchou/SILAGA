import base64
import json
import time
import urllib.request as urllib2
from datetime import datetime
from xml.etree.ElementTree import fromstring
import entry_updater as updater
import requests
import classifier_rest as classifier
import hbase_rest as hbase 

from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS, cross_origin
from apscheduler.schedulers.background import BackgroundScheduler

from flask_cors import CORS, cross_origin


# instantiate flask app
app = Flask(__name__,static_folder='docx')
CORS(app)

ENTRY_UPDATER = updater.EntryUpdater()

DELAY = 5*60
SOLR = 'http://localhost:8983/'
IP_CLASSIFIER = 'http://localhost:18881/'

@app.route("/update-new-entry/",methods=['POST'])
@cross_origin()
def update_new_entry():
    input_request = request.get_json()
    print(input_request)
    ENTRY_UPDATER.updater_helper2(
        input_request['earlier-time'],
        input_request['later-time'],
        input_request['interval']
        )
    # updater.main_caller()
    resp = Response({}, status=200, mimetype='application/json') 
    return resp





if __name__ == '__main__':
    IP = '10.32.6.225'
    PORT = 18881
    IP = '127.0.0.1'
    PORT = 5002
    # scheduler = BackgroundScheduler(standalone=True)
    # job = scheduler.add_job(main_caller, 'interval', minutes=1, id='id_scheduler')
    # try:
    #     # print("start")
    #     scheduler.start()
    # except (KeyboardInterrupt):
    #     logger.debug('Got SIGTERM! Terminating...')
    #     print("EXIT")
    app.run(debug=True, port=PORT, host=IP, use_reloader=False)
    # scheduler.remove_job('id_scheduler')
    # print("EXIT 2")