
import uuid
from datetime import datetime
from flask import abort, Blueprint, flash, redirect, render_template, request, url_for
from green_server import db, bcrypt
from green_server.models import User, Device, Parameter, DataPoint
from green_server.settings.forms import RegistrationForm, DeviceForm, ParameterForm, DeleteForm, UploadDataForm
from green_server.settings.utils import admin_required

settings = Blueprint('settings', __name__)

@settings.route('/configuration', methods=['GET', 'POST'])
@admin_required
def configuration():
    # return user/ device/ parameter configuration page
    users = User.query.all()
    parameters = Parameter.query.all()
    devices = Device.query.all()

    return render_template('configuration.html', title='Configuration', parameters=parameters, users=users, devices=devices)

# User
@settings.route('/user/new', methods=['GET', 'POST'])
@admin_required
def new_user():
    # return create user page
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if User.query.filter_by(username=form.user.data).first():
                flash(f'User: "{form.user.data}" already exists!', 'danger')
            elif form.password.data != form.confirm_password.data:
                flash(f'Passwords do not match!', 'danger')
            else:
                hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(
                    public_id=int(uuid.uuid4().time_low), 
                    username=form.user.data,
                    password=hashed_pw, 
                    admin=False
                    )
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash(f'User: "{user.username}" created!', 'success')
                except:
                    flash(f'User create failure!', 'danger')
                return redirect(url_for('settings.configuration'))
        else:
            flash(f'Form invalid! Check fields!', 'danger')

    return render_template('user.html', title='Create User', form=form, devices=Device.query.all())

@settings.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def user(user_id):
    # return edit device page
    user = User.query.filter_by(public_id=user_id).first()
    if not user:
        abort(404)

    form = RegistrationForm()
    if form.validate_on_submit():
        user.username = form.user.data
        user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        try:
            db.session.commit()
            flash(f'User: "{user.username}" changed!', 'success')
        except:
            flash(f'User edit failed!', 'danger')
        return redirect(url_for('settings.configuration'))
    elif request.method == 'GET':
        form.user.data = user.username
    else:
        flash(f'User edit failure! Check Fields!', 'danger')
    return render_template('user.html', title=f'Edit User - "{user.username}"', form=form, devices=Device.query.all())

@settings.route('/user/<int:user_id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_user(user_id):
    # return flash delete success
    user = User.query.filter_by(public_id=user_id).first()
    if not user or user.admin:
        abort(404)
    
    delete_info = 'WARNING: Deleting a user will log the user out!'

    form = DeleteForm()
    if form.validate_on_submit():
        if form.name.data == user.username and form.confirm.data:
            try:
                db.session.delete(user)
                db.session.commit()
                flash(f'User: "{user.username}" deleted!', 'danger')
            except:
                flash(f'User delete failure!', 'danger')
            return redirect(url_for('settings.configuration'))
        else:
            flash(f'Please check fields', 'danger')

    return render_template('confirm_delete.html', title=f'Delete User - "{user.username}"', form=form, delete_info=delete_info, devices=Device.query.all())

# Device
@settings.route('/device/new', methods=['GET', 'POST'])
@admin_required
def new_device():
    # return create device page
    form = DeviceForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if Device.query.filter_by(name=form.name.data).first():
                flash(f'Device: "{form.name.data}" already exists!', 'danger')
            else:
                dev = Device(
                    public_id=int(uuid.uuid4().time_low), 
                    name=form.name.data.lower(), 
                    descr=form.descr.data, 
                    collection_method=form.collection_method.data
                    )
                try:
                    db.session.add(dev)
                    db.session.commit()
                    flash(f'Device: "{dev.name}" created!', 'success')
                except:
                    flash(f'Device create failure!', 'danger')
                return redirect(url_for('settings.configuration'))
        else:
            flash(f'Form invalid! Check fields!', 'danger')

    return render_template('device.html', title='Create Device', form=form, devices=Device.query.all())

@settings.route('/device/<int:device_id>/edit', methods=['GET', 'POST'])
@admin_required
def device(device_id):
    # return edit device page
    dev = Device.query.filter_by(public_id=device_id).first()
    if not dev:
        abort(404)
    
    form = DeviceForm()
    if form.validate_on_submit():
        dev.name, dev.descr = form.name.data, form.descr.data
        dev.collection_method = form.collection_method.data
        try:
            db.session.commit()
            flash(f'Device: "{dev.name}" changed!', 'success')
        except:
            flash(f'Device edit failed!', 'danger')
        return redirect(url_for('settings.configuration'))
    elif request.method == 'GET':
        form.name.data, form.descr.data = dev.name, dev.descr
        form.collection_method.data = dev.collection_method
    else:
        flash(f'Device edit failure!', 'danger')
    return render_template('device.html', title=f'Edit Device - "{dev.name}"', form=form, devices=Device.query.all())

@settings.route('/device/<int:device_id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_device(device_id):
    # return flash delete success
    dev = Device.query.filter_by(public_id=device_id).first()
    if not dev:
        abort(404)

    delete_info = 'WARNING: Deleting a device will also delete parameters and data associated with the device!'

    form = DeleteForm()
    if form.validate_on_submit():
        if form.name.data == dev.name and form.confirm.data:
            try:
                for param in dev.parameters:
                    DataPoint.query.filter_by(parameter=param).delete()
                    db.session.delete(param)
                db.session.delete(dev)
                db.session.commit()
                flash(f'Device: "{dev.name}" deleted!', 'danger')
            except:
                flash(f'Device delete failure!', 'danger')
            return redirect(url_for('settings.configuration'))
        else:
            flash(f'Please check fields', 'danger')

    return render_template('confirm_delete.html', title=f'Delete Device - "{dev.name}"', form=form, delete_info=delete_info, devices=Device.query.all())

# Parameter
@settings.route('/parameter/new', methods=['GET', 'POST'])
@admin_required
def new_parameter():
    # return create parameter page
    form = ParameterForm()
    form.device.choices = [(dev.public_id, dev.name) for dev in Device.query.all()]
    form.device.default = form.device.choices[0][0]
    if request.method == 'POST':
        if form.validate_on_submit():
            dev = Device.query.filter_by(public_id=form.device.data).first()
            if Parameter.query.filter_by(name=form.name.data).filter_by(device=dev).first():
                flash(f'Parameter: "{form.name.data}" already exists!', 'danger')
            else:
                if not dev:
                    abort(400)
                param = Parameter(
                    public_id=int(uuid.uuid4().time_low), 
                    name=form.name.data, 
                    descr=form.descr.data,
                    device=dev
                    )
                try:
                    db.session.add(param)
                    db.session.commit()
                    flash(f'Parameter: "{param.name}" created!', 'success')
                except:
                    flash(f'Parameter create failure!', 'danger')
                return redirect(url_for('settings.configuration'))
        else:
            flash(f'Form invalid! Check fields!', 'danger')
    return render_template('parameter.html', title='Create Parameter', form=form, devices=Device.query.all())

@settings.route('/parameter/<int:parameter_id>/edit', methods=['GET', 'POST'])
@admin_required
def parameter(parameter_id):
    # return parameter edit page
    param = Parameter.query.filter_by(public_id=parameter_id).first()
    if not param:
        abort(404)

    form = ParameterForm()
    form.device.choices = [(dev.public_id, dev.name) for dev in Device.query.all()]
    if form.validate_on_submit():
        dev = Device.query.filter_by(public_id=form.device.data).first()
        if not dev:
            abort(400)
        else:
            param.name, param.descr, param.device = form.name.data, form.descr.data, dev
            try:
                db.session.commit()
                flash(f'Parameter: "{param.name}" changed!', 'success')
            except:
                flash(f'Parameter edit failure!', 'danger')
        return redirect(url_for('settings.configuration'))
    elif request.method == 'GET':
        form.name.data, form.descr.data = param.name, param.descr
    else:
        flash(f'Parameter edit failure! Check fields!', 'danger')
    return render_template('parameter.html', title=f'Edit Parameter - "{param.name}"', form=form, devices=Device.query.all())

@settings.route('/parameter/<int:parameter_id>/delete', methods=['GET', 'POST'])
@admin_required
def delete_parameter(parameter_id):
    # return flash delete success
    param = Parameter.query.filter_by(public_id=parameter_id).first()
    if not param:
            abort(404)

    delete_info = 'WARNING: Deleting a parameter will also delete all data associated with the parameter!'
    
    form = DeleteForm()
    if form.validate_on_submit():
        if form.name.data == param.name and form.confirm.data:
            try:
                DataPoint.query.filter_by(parameter=param).delete()
                db.session.delete(param)
                db.session.commit()
                flash(f'Parameter: "{param.name}" + data deleted!', 'danger')
            except:
                flash(f'Parameter delete failure!', 'danger')
            return redirect(url_for('settings.configuration'))
        else:
            flash(f'Please check fields', 'danger')

    return render_template('confirm_delete.html', title=f'Delete Parameter - "{param.name}"', form=form, delete_info=delete_info, devices=Device.query.all())

# Upload data
@settings.route('/upload', methods=['GET', 'POST'])
@admin_required
def upload_data():
    form = UploadDataForm()
    if request.method == 'POST':
        try:
            # read and format csv data
            file_data = form.data_file.data.read().decode()
            data = [row.split(',') for row in file_data.split('\r\n') if row != '']
            for row in data:
                param = Parameter.query.filter_by(public_id=row[0]).first()
                timestamp = datetime.fromtimestamp(int(row[1]))
                value = float(row[2])
                data_point = DataPoint(timestamp=timestamp, value=value, parameter=param)
                db.session.add(data_point)
            db.session.commit()
            flash('Data upload success!', 'success')
        except:
            flash('Data upload error!', 'danger')
        return redirect(url_for('settings.configuration'))

    return render_template('upload_data.html', title='Upload Data', form=form, devices=Device.query.all())
