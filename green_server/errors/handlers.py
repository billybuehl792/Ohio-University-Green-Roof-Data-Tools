
from flask import Blueprint, render_template
from green_server.models import Device

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(400)
def error_400(e):
    code = 400
    m = f'{code}: Bad Request!'
    return render_template('construction.html', title=code, m=m, devices=Device.query.all()), code

@errors.app_errorhandler(401)
def error_401(e):
    code = 401
    m = f'{code}: Access Denied!'
    return render_template('construction.html', title=code, m=m, devices=Device.query.all()), code

@errors.app_errorhandler(403)
def error_403(e):
    code = 403
    m = f'{code}: Resource Forbidden!'
    return render_template('construction.html', title=code, m=m, devices=Device.query.all()), code

@errors.app_errorhandler(404)
def error_404(e):
    code = 404
    m = f'{code}: Page not found!'
    return render_template('construction.html', title=code, m=m, devices=Device.query.all()), code

@errors.app_errorhandler(405)
def error_405(e):
    code = 405
    m = f'{code}: Method not allowed!'
    return render_template('construction.html', title=code, m=m, devices=Device.query.all()), code

@errors.app_errorhandler(500)
def error_500(e):
    code = 500
    m = f'{code}: Something went wrong... This is our fault though...'
    return render_template('construction.html', title=code, m=m, devices=Device.query.all()), code
