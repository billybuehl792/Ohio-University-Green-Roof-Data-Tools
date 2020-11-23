# utils.py - utilities for 'api' routes

import jwt
from datetime import datetime, timedelta
from flask import current_app, jsonify, request, abort
from flask_login import current_user
from functools import wraps
from green_server import db
from green_server.models import User, Device, Parameter, DataPoint

# decorators
def token_required(original_func):
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')   # http://localhost:5000/route?token=a12vwqk21mfwefn1o12
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return original_func(*args, **kwargs)
    return wrapper

def token_or_login_required(original_func):
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return original_func(*args, **kwargs)
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return original_func(*args, **kwargs)
    return wrapper

# query tools
def retrieve_data(parameter_id, parameter_name, t1, t2, t_string):
    # datatime objects from epoch times
    data_start = datetime.fromtimestamp(t1)
    data_end = datetime.fromtimestamp(t2)

    if t_string:
        # fetch averages
        query = db.session.query(DataPoint.parameter_id, DataPoint.timestamp, db.func.avg(DataPoint.value), db.func.min(DataPoint.value), db.func.max(DataPoint.value)).filter(DataPoint.parameter_id==parameter_id).filter(DataPoint.timestamp > data_start).filter(DataPoint.timestamp < data_end).group_by(db.func.strftime(t_string[1], DataPoint.timestamp))
        data = [
            {'type': 'average', 'parameter_name': parameter_name, 'data_points': []},
            {'type': 'range', 'parameter_name': parameter_name, 'data_points': []}
        ]
        for point in query.all():
            if t_string[0] == 'Daily':
                timestamp = str(point[1].replace(hour=0, minute=0, second=0, microsecond=0))
            else:
                timestamp = str(point[1].replace(minute=0, second=0, microsecond=0))
            data[0]['data_points'].append({'timestamp': timestamp, 'value': point[2]})
            data[1]['data_points'].append({'timestamp': timestamp, 'value': [point[3], point[4]]})
    else:
        # fetch all data
        query = db.session.query(DataPoint.parameter_id, DataPoint.timestamp, DataPoint.value).filter(DataPoint.parameter_id==parameter_id).filter(DataPoint.timestamp > data_start).filter(DataPoint.timestamp < data_end)
        data = [
            {'type': 'all', 'parameter_name': parameter_name, 'data_points': []}
        ]
        for point in query.all():
            data[0]['data_points'].append({'timestamp': str(point[1].replace(microsecond=0)), 'value': point[2]})

    # return all formatted data from query
    return data

def query_data(parameters, t1, t2, t_string):
    ids, params, descr = [], [], []
    for p in parameters:
        ids.append(p.public_id)
        params.append(p.name)
        descr.append(p.descr)

    if t_string:
        title_descr = f'{t_string[0]} Average'
    else:
        title_descr = 'All'

    # output dictionary
    output = {
        'parameter_ids': ids,
        'parameters': params,
        'data_descr': (', ').join(descr),
        'data_title': f'{title_descr} - {(", ").join(params)}',
        'data': []
    }

    # query db for parameter data - add to output['data']
    for param in parameters:
        data = retrieve_data(param.id, param.name, t1, t2, t_string)
        for d in data:
            output['data'].append(d)

    # return output dictionary
    return output
