# forms.py - forms for 'settings'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    user = StringField('Username', validators=[DataRequired(), Length(min=7, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=7, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8, max=50), EqualTo('password')])
    create = SubmitField('Submit User')

    def __repr__(self):
        return 'RegistrationForm(user, password, confirm_password, create)'

class DeviceForm(FlaskForm):
    name = StringField('Device Name (max: 32)', validators=[DataRequired(), Length(min=1, max=32)])
    descr = StringField('Device Description', validators=[DataRequired(), Length(min=1, max=254)])
    collection_method = StringField('Data Collection Method (max: 32)', validators=[DataRequired(), Length(min=1, max=32)])
    submit = SubmitField('Submit Device')

    def __repr__(self):
        return 'DeviceForm(name, descr, collection_method, submit)'

class ParameterForm(FlaskForm):
    name = StringField('Parameter Name (max: 32)', validators=[DataRequired(), Length(min=1, max=32)])
    descr = StringField('Parameter Description', validators=[DataRequired(), Length(min=1, max=254)])
    device = RadioField('Parameter Device', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit Parameter')

    def __repr__(self):
        return 'ParameterForm(name, descr, device, submit)'

class DeleteForm(FlaskForm):
    name = StringField('Please type full item name to confirm delete', validators=[DataRequired(), Length(min=1, max=32)])
    confirm = BooleanField('I want to permanently delete this item')
    delete = SubmitField('Permanently Delete Item')

    def __repr__(self):
        return 'DeleteForm(name, password, confirm, delete)'

class UploadDataForm(FlaskForm):
    data_file = FileField('Data File', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only!')])
    upload = SubmitField('Upload Data')

    def __repr__(self):
        return 'UploadDataForm(parameter, upload)'
