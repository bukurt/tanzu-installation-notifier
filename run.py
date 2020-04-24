# -*- coding: utf-8 -*-
import requests
import json
import time
import datetime
import subprocess
import os
import re

try:
    os.chdir('/app')
    # Params
    opsman_ip = str(os.environ['OPSMAN_IP'])
    opsman_url = 'https://'+opsman_ip+'/api/v0/installations'
    slack_url = os.environ['SLACK_URL']
    slack_headers = {
        'Content-type': 'application/json',
    }
    sleep_time = int(os.environ['API_REQUEST_CYCLE'])            # seconds
    run_inform_period = int(os.environ['RUNNING_INFORM_PERIOD'])    # times sleep_time
    
    # Get access-token
    access_token = ''
    headers = ''
    
    # Display info
    print(str(datetime.datetime.utcnow()), end=' -- ')
    disp='Ops Manager: '+str(opsman_ip)
    print(disp)    
    print(str(datetime.datetime.utcnow()), end=' -- ')
    disp='Access token: '+str(access_token)
    print(disp)
    
    last_inform_id = ''
    last_inform_status = ''
    counter = 0
    while True:
        response = requests.get(opsman_url, headers=headers, verify=False)
        if response.status_code != 200:
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print(str(response.content))
            f = open('error.log', 'w+')
            f.write(str(response.content))
            f.close()
            print(str(datetime.datetime.utcnow()), end=' -- ')
            msg=("%s ERROR %s") % (str(datetime.datetime.utcnow), str(response.content))
            print(msg)
            # Get access-token
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print('Getting new access token')
            cmd = '/app/get-uaa-token.sh'
            access_token = str(subprocess.check_output(['sh',cmd]))
            access_token = access_token.rstrip("\n\r")
            access_token = access_token.split('\'')[1]
            print('Access token: '+access_token)
            headers = {
                'Authorization': 'Bearer '+access_token,
            }
            continue
            
        resp_json = json.loads(response.content)
        last_run=resp_json['installations'][0]
        day_passed = datetime.datetime.today()  - datetime.datetime.strptime(last_run['started_at'], "%Y-%m-%dT%H:%M:%S.%fZ")

        ins_log_url = opsman_url + '/' + str(last_run['id']) + '/logs'
        ins_log_resp = requests.get(ins_log_url , headers=headers, verify=False)
        ins_log = str(ins_log_resp.content)
        ins_log = ins_log.split('\\n')
        r = re.compile(r"^=====")
        ins_log_p1 = list(filter(r.match, ins_log))[-1]
        ins_log_sum = ins_log_p1 + '\n...\n' + ins_log[-3] + '\n' + ins_log[-2] + '\n' + ins_log[-1]
        ins_log_sum = re.sub(r"[^a-zA-Z0-9\n.,/()-]+", ' ',ins_log_sum)

        if last_run['status'] == 'running':
            sbj = 'Tanzu Update in Progress - '+opsman_ip
            msg=("""Installation RUNNING - %s
                 Timestamp: %s
                 Id: %s
                 Started: %s
                 Finished: %s
                 Status: %s
                 Last Log Summary:
                 %s
                 """) % (str(opsman_ip),str(datetime.datetime.utcnow()),last_run['id'],last_run['started_at'],last_run['finished_at'],last_run['status'],ins_log_sum)
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print(msg)
            if last_run['status'] != last_inform_status:
                last_inform_status = last_run['status']
                print(str(datetime.datetime.utcnow()), end=' -- ')
                print('Sending slack notification.')
                slack_data = '{"text":"'+msg+'"}'
                r = requests.post(slack_url, headers=slack_headers, data=slack_data, verify=False)
                print(str(r.content))
            elif counter % run_inform_period == 0:
                print(str(datetime.datetime.utcnow()), end=' -- ')
                print('Sending slack notification.')
                slack_data = '{"text":"'+msg+'"}'
                r = requests.post(slack_url, headers=slack_headers, data=slack_data, verify=False)
                print(str(r.content))
        elif last_run['status'] == 'failed' and day_passed.days < 1 :
            last_inform_status = last_run['status']
            sbj = 'Tanzu Updadate Failed - '+opsman_ip
            msg=("""Installation FAILED - %s
                 Id: %s
                 Started: %s
                 Finished: %s
                 Status: %s
                 Last Log Summary:
                 %s
                 """) % (str(opsman_ip),last_run['id'],last_run['started_at'],last_run['finished_at'],last_run['status'],ins_log_sum)
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print(msg)
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print("last_inform_id: "+str(last_inform_id))
            print("last_run_id: "+str(last_run['id']))
            if str(last_inform_id) != str(last_run['id']):
                last_inform_id = str(last_run['id'])
                print('Sending slack notification.')
                slack_data = '{"text":"'+msg+'"}'
                r = requests.post(slack_url, headers=slack_headers, data=slack_data, verify=False)
                print(str(r.content))
        elif last_run['status'] == 'succeeded' and day_passed.days < 1 :
            last_inform_status = last_run['status']
            sbj = 'Tanzu Updadate Succeeded - '+opsman_ip
            msg=("""Installation SUCCESS - %s
                 Id: %s
                 Started: %s
                 Finished: %s
                 Status: %s
                 """) % (str(opsman_ip),last_run['id'],last_run['started_at'],last_run['finished_at'],last_run['status'])
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print(msg)
            print(str(datetime.datetime.utcnow()), end=' -- ')
            print("last_inform_id: "+str(last_inform_id))
            print("last_run_id: "+str(last_run['id']))
            if str(last_inform_id) != str(last_run['id']):
                last_inform_id = str(last_run['id'])
                print('Sending slack notification.')
                slack_data = '{"text":"'+msg+'"}'
                r = requests.post(slack_url, headers=slack_headers, data=slack_data, verify=False)
                print(str(r.content))
        print(str(datetime.datetime.utcnow()), end=' -- ')
        print('Sleeping '+str(sleep_time)+' seconds...')    
        time.sleep(sleep_time)
        counter += 1
        
except Exception as e:
    print(str(datetime.datetime.utcnow()), end=' -- ')
    print(e)

