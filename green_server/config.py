
import os
import json

config_file = '/etc/ougr_config.json'
with open(config_file, 'r') as f:
    config = json.load(f)

basedir = os.path.abspath(os.path.dirname(__file__))
db = 'reduced_data.db'

class Config(object):
    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, db)}'
    DATA_UPLOADS = f'{os.path.join(basedir, "static/data_upload")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False
