import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
	APP_NAME = "Bioinf Toolbox"
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret3'
	ALLOWED_EXTENSIONS = set(['fasta', 'fastq'])
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	UPLOAD_FOLDER = '/userUploads'

	# CELERY_BROKER_URL = 'amqp://localhost:5672/'
	# CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

	CELERY_BROKER_URL = os.environ.get('RABBITMQ_SERVICE_SERVICE_HOST')
	CELERY_RESULT_BACKEND = 'rpc'

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 't0p s3cr3t'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    Testing = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,

	'default': DevelopmentConfig
}
