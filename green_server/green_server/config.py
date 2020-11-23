
import os
import json

config_file = '/etc/config/configuration.json'
with open(config_file, 'r') as f:
    config = json.load(f)

class Config:

    SECRET_KEY = config.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    CSRF_ENABLED = True
    USER_ENABLE_EMAIL = False
