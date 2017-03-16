import os

basedir = os.path.abspath(os.path.dirname(__file__))

# class Auth:
# 	CLIENT_ID = ('218586408121-ukk13e2hc4trsg809mem2b1b7t85dhk5.apps.googleusercontent.com')
# 	CLIENT_SECRET = ('REm6Ji7tX7Pv9X4tvjbffzpE')
# 	REDIRECT_URI = 'https://localhost:5000/gCallback'
# 	AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
# 	TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
# 	USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'


class Config:
	APP_NAME = "Bioinf Toolbox"
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret3'
	ALLOWED_EXTENSIONS = set(['fasta', 'fastq'])
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	UPLOAD_FOLDER = '/home/olof/courses/exjobb/projExjobb/scalableCloudCommunity/userUploads'

	# CELERY_BROKER_URL = 'redis://172.17.0.2:6379/0'
	# CELERY_RESULT_BACKEND = 'redis://172.17.0.2:6379/0'

	CELERY_BROKER_URL = 'redis://:devpassword@redis:6379/0'
	CELERY_RESULT_BACKEND = 'redis://:devpassword@redis:6379/0'

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
