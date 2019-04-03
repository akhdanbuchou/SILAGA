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
scheduler = BackgroundScheduler(standalone=True)

def updater_caller():
    return ENTRY_UPDATER.periodic_updater_helper()

@app.route("/set-latest-entry-time/",methods=['POST'])
@cross_origin()
def set_latest_entrytime():
    input_request = request.get_json()
    entry_status = ENTRY_UPDATER.set_latest_entry_time(
        input_request['date-entry']
        )
    return Response(
        json.dumps({'entry-status':entry_status}), 
        status=200, 
        mimetype='application/json'
        ) 

@app.route("/stop-current-update/",methods=['GET'])
@cross_origin()
def stop_current_update():
    entry_status = ENTRY_UPDATER.halt_update()
    resp = Response(
        json.dumps({'entry-status':entry_status}), 
        status=200, 
        mimetype='application/json'
        ) 
    return resp

@app.route("/allow-next-update/",methods=['GET'])
@cross_origin()
def allow_next_update():
    entry_status = ENTRY_UPDATER.allow_update()
    resp = Response(
        json.dumps({'entry-status':entry_status}), 
        status=200, 
        mimetype='application/json'
        ) 
    return resp

@app.route("/update-stop/",methods=['GET'])
@cross_origin()
def stop_update():
    try:
        scheduler.remove_job('id_scheduler')
        entry_status = ENTRY_UPDATER.switch_update_off()
    except:
        entry_status = 'Failed'
    resp = Response(
        json.dumps({'entry-status':entry_status}), 
        status=200, 
        mimetype='application/json'
        ) 
    return resp

@app.route("/update-continue/",methods=['GET'])
@cross_origin()
def continue_update():
    try:
        job = scheduler.add_job(updater_caller, 'interval', minutes=1, id='id_scheduler')
        # scheduler.start()
        entry_status = ENTRY_UPDATER.switch_update_on()
    except:
        entry_status = 'Failed'
    resp = Response(
        json.dumps({'entry-status':entry_status}), 
        status=200, 
        mimetype='application/json') 
    return resp

@app.route("/update-new-entry/",methods=['POST'])
@cross_origin()
def update_new_entry():
    input_request = request.get_json()
    ENTRY_UPDATER.updater_helper(
        input_request['earlier-time'],
        input_request['later-time'],
        input_request['interval']
        )
    # updater.main_caller()
    resp = Response({}, status=200, mimetype='application/json') 
    return resp

@app.route("/stop-scheduler/",methods=['GET'])
@cross_origin()
def stop_scheduler():
    scheduler.remove_job('id_scheduler')
    resp = Response({}, status=200, mimetype='application/json') 
    return resp

# def updater_caller():
#     return ENTRY_UPDATER.periodic_updater_helper()

@app.route("/update-periodic-entry/",methods=['GET'])
@cross_origin()
def update_periodic_entry():
    resp = Response({}, status=200, mimetype='application/json') 
    return resp




if __name__ == '__main__':
    IP = '10.32.6.225'
    PORT = 18881
    IP = '127.0.0.1'
    PORT = 5002
    # scheduler = BackgroundScheduler(standalone=True)
    # job = scheduler.add_job(updater_caller, 'interval', minutes=1, id='id_scheduler')
    try:
        scheduler.start()
    except (KeyboardInterrupt):
        logger.debug('Got SIGTERM! Terminating...')
        print("EXIT")
    app.run(debug=True, port=PORT, host=IP, use_reloader=False)

    try:
        scheduler.remove_job('id_scheduler')
    except:
        pass
    # print("EXIT 2")