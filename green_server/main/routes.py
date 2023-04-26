# routes.py - 'main' routes

from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from green_server import db, bcrypt
from green_server.main.forms import LoginForm
from green_server.models import User, Device, Parameter, DataPoint

main = Blueprint('main', __name__)

@main.route('/login', methods=['GET', 'POST'])
def login():
    # return login form then redirect to home
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.user.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash('Email or password incorrect', 'danger')
    return render_template('login.html', title='login', form=form)

@main.route('/logout')
def logout():
    # logout current user then redirect to /login
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/')
def home():
    # return home page
    return render_template('home.html', title='Home', devices=Device.query.all())

@main.route('/latest_data/<int:device_id>')
def latest_data(device_id):
    # return device page with list of parameters collected by device
    device = Device.query.filter_by(public_id=device_id).first()
    if not device:
        abort(404)
    parameters = Parameter.query.filter_by(device_id=device.id).all()
    
    # most recent data of each 'param' of device
    d = []
    for param in parameters:
        # query first data point of 'param' from timestamp descending table
        if DataPoint.query.filter_by(parameter_id=param.id).first():
            data = db.session.query(DataPoint).filter(DataPoint.parameter_id==param.id).order_by(DataPoint.timestamp.desc()).first()
            d.append(
                {
                    'id': param.public_id,
                    'name': param.name,
                    'value': round(data.value, 3),
                    'timestamp': data.timestamp,
                    'descr': param.descr
                }
            )
    return render_template('latest_data.html', title=device.name, device=device, d=d, devices=Device.query.all())

@main.route('/graph')
@login_required
def graph():
    # return graphs of selected parameters
    devices = Device.query.all()
    parameters = Parameter.query.all()
    title = "Combined Graphs"

    return render_template('graph.html', title=title, parameters=parameters, param_length=len(parameters), devices=devices)

@main.route('/graph_parameter/<int:parameter_id>')
@login_required
def graph_parameter(parameter_id):
    # return graph specific device parameter
    parameter = Parameter.query.filter_by(public_id=parameter_id).first()
    if not parameter:
        abort(404)
    device = Device.query.get_or_404(parameter.device_id)
    title = f'{device.name}.{parameter.name}'

    return render_template('graph_parameter.html', title=title, parameter=parameter, devices=Device.query.all())

@main.route('/account')
@login_required
def account():
    return render_template('account.html', title=current_user.username, devices=Device.query.all())
