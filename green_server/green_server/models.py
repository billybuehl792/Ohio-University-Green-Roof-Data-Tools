# models.py - database structure

from green_server import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    admin = db.Column(db.Boolean)

    def __repr__(self):
        return f'User("{self.username}")'


class Device(db.Model):
    __tablename__ = 'devices'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    descr = db.Column(db.String(254), nullable=False)
    collection_method = db.Column(db.String(32), nullable=False)
    parameters = db.relationship('Parameter', backref='device')

    def __repr__(self):
        return f'Device("{self.name}", "{self.collection_method}")'


class Parameter(db.Model):
    __tablename__ = 'parameters'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    descr = db.Column(db.Unicode, nullable=False)
    data_points = db.relationship('DataPoint', backref='parameter')
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)

    def __repr__(self):
        return f'Parameter("{self.name}", "{self.descr}")'


class DataPoint(db.Model):
    __tablename__ = 'data_points'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'), nullable=False, index=True)

    def __repr__(self):
        return f'DataPoint("{self.timestamp}", "{self.parameter_id}", "{self.value}")'
