# utils.py - utilities for configuration pages

from flask import abort, current_app
from flask_login import current_user
from functools import wraps

def admin_required(original_func):
    @wraps(original_func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.admin:
            return original_func(*args, **kwargs)
        else:
            abort(401)
    return wrapper
