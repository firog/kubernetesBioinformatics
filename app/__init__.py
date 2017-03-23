import os
from flask import Flask
from flask_bootstrap import Bootstrap
from config import config, Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from celery import Celery

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

# CELERY_BROKER_URL = os.environ.get('RABBITMQ_SERVICE_SERVICE_HOST')
# celery = Celery(__name__, broker='amqp://guest@%s' % os.environ.get('RABBITMQ_SERVICE_SERVICE_HOST'))

celery = Celery(__name__)

def create_app(config_name=(os.getenv('FLASK_CONFIG') or 'default')):
	app = Flask(__name__)
	app.config.from_object(config[config_name])

	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	moment.init_app(app)
	celery.conf.update(app.config)
	celery.conf['CELERY_BROKER_URL'] = os.environ.get('RABBITMQ_SERVICE_SERVICE_HOST') or 'default'
	# print ("after app creation:"+celery.conf['CELERY_BROKER_URL']+"\n")

	from .pages import pages as pages_blueprint
	app.register_blueprint(pages_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .uploads import uploads as uploads_blueprint
	app.register_blueprint(uploads_blueprint)

	from .tools import tools as tools_blueprint
	app.register_blueprint(tools_blueprint, url_prefix='/tools')

	from api_1_0 import api1 as api_blueprint
	app.register_blueprint(api_blueprint, url_prefix='/api/1')

	return app
