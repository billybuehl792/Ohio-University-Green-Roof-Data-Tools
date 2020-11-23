from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from green_server.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from green_server.main.routes import main
    from green_server.settings.routes import settings
    from green_server.api.routes import api
    from green_server.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(settings)
    app.register_blueprint(api)
    app.register_blueprint(errors)

    return app