
import jwt
from datetime import datetime, timedelta
from flask import abort, Blueprint, current_app, jsonify, request
from green_server import bcrypt, db
from green_server.api.utils import token_required, token_or_login_required, query_data, retrieve_data
from green_server.models import User, Device, Parameter, DataPoint

api = Blueprint('api', __name__)

@api.route('/get_key')
def get_key():
    try:
        auth = request.authorization
        user = User.query.filter_by(username=auth.username).first()
    except:
        return jsonify({'message': 'Bad Request!'}), 400
    if user.admin and bcrypt.check_password_hash(user.password, auth.password):
        exp = datetime.utcnow() + timedelta(minutes=10)
        # test verify signature: https://jwt.io/
        token = jwt.encode({'user': auth.username, 'exp': exp}, current_app.config['SECRET_KEY'])
        return jsonify({'message': 'Verified!', 'token': token.decode('UTF-8'), 'expires': str(exp)})

    return jsonify({'message': 'Invalid Credentials'}), 401

@api.route('/data')
@token_or_login_required
def data():
    # return json formatted data
    # process request parameters
    data = request.args
    try:
        parameter_ids = [int(p) for p in data.getlist('parameter_ids')]
        averages = int(data.get('averages'))
        t1 = int(data.get('data_start'))
        t2 = int(data.get('data_end'))
    except:
        return jsonify({'message': 'Bad Request!'}), 400

    # query parameter
    parameters = []
    for param in parameter_ids:
        parameters.append(Parameter.query.filter_by(public_id=param).first())

    # set default t_string
    t_string = None

    # determine t_string if averages specified
    if averages == 1:
        hours = round((t2 - t1) / 3_600)
        if hours > 500:
            t_string = ('Hourly', '%Y-%m-%d %H')            # Hourly averages
            if hours > 3000:
                t_string = ('Daily', '%Y-%m-%d')            # Daily averages
    
    # return json data to '/data'
    return jsonify(query_data(parameters, t1, t2, t_string)), 200

@api.route('/push', methods=['POST'])
@token_required
def push():
    data = request.args
    try:
        parameter = Parameter.query.filter_by(public_id=int(data.get('parameter_id'))).first()
        timestamp = datetime.fromtimestamp(int(data.get('timestamp')))
        value = float(data.get('value'))
        data_point = DataPoint(timestamp=timestamp, value=value, parameter=parameter)
        db.session.add(data_point)
        db.session.commit()
        return jsonify({'message': f'{data_point.value} added to {parameter.name}!'}), 200
    except:
        return jsonify({'message': 'Bad Request: parameter_id, timestamp, value, token'}), 400
