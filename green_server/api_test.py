#!python3

import json
from datetime import datetime
import requests
from requests.auth import HTTPBasicAuth
import sys
from random import random

def get_token(user, password):
    page = 'http://ougr.its.ohio.edu/get_key'
    auth = HTTPBasicAuth(user, password)
    req = requests.get(page, auth=auth)
    result = json.loads(req.content.decode('UTF-8'))
    return result.get('token')

def get_data(token='', parameter_ids=[], averages=0, data_start=round(datetime.now().timestamp()), data_end=round(datetime.now().timestamp())):
    page = 'http://ougr.its.ohio.edu/data'
    params = {
        'parameter_ids': parameter_ids,     # parameter list
        'averages': averages,               # no averages - all data
        'data_start': data_start,           # start of data
        'data_end': data_end,               # end of data
        'token': token                      # retrieved token
        }
    req = requests.get(page, params=params)
    try:
         return json.loads(req.content.decode('UTF-8'))
    except:
        return None

def data_push(token='', parameter_id=0, timestamp=round(datetime.now().timestamp()), value=0):
    page = 'http://ougr.its.ohio.edu/push'
    params = {
        'parameter_id': parameter_id,
        'timestamp': timestamp,
        'value': value,
        'token': token
    }
    req = requests.post(page, params=params)
    response = json.loads(req.content.decode('UTF-8'))

    return response.get('message')


if __name__ == '__main__':
    # retrieve token
    try:
        # username = sys.argv[1]
        # password = sys.argv[2]
        username = 'itsclass'
        password = 'class115#'
    except IndexError:
        print('provide: "username" "password"')
        sys.exit()

    token = get_token(username, password)
    print(token)
    parameter_ids = [1176000961, 3002308254]
    data_start = 1599944591
    data_end = 1599945191

    # push a random data point
    # push_data_point = data_push(token=token, parameter_id=parameter_ids[0], value=random()*100)
    # print(push_data_point.get('message'))

    # retrieve data
    # data = get_data(token=token, parameter_ids=parameter_ids, data_start=data_start, data_end=data_end)
    # print(data)
