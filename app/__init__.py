from flask import Flask
from flask_bootstrap import Bootstrap
from config import config
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	bootstrap.init_app(app)
	db.init_app(app)

	from .pages import pages as pages_blueprint
	app.register_blueprint(pages_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	return app
