from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
from flask import request, url_for
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), nullable=False, unique=True, index=True)
	username = db.Column(db.String(64), nullable=False, unique=True, index=True)
	is_admin = db.Column(db.Boolean)
	password_hash = db.Column(db.String(128))
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	bio = db.Column(db.Text())
	member_sinze = db.Column(db.DateTime(), default=datetime.utcnow)
	avatar_hash = db.Column(db.String(32))
	posts = db.relationship('Post', lazy='dynamic', backref='author')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.email is not None and self.avatar_hash is None:
			self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

	@property
	def password(self):
		raise AttributeError('Password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
			hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
			url=url, hash=hash, size=size, default=default, rating=rating)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False)
	content = db.Column(db.String(512), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	date = db.Column(db.DateTime(), default=datetime.utcnow)

class Task(db.Model):
	__tablename__ = 'tasks'
	id = db.Column(db.Integer, primary_key=True)
	# user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	task_id = db.Column(db.String(512))
	task_state = db.Column(db.String(32))
	task_name = db.Column(db.String(32))
	result = db.Column(db.String)
	# created_by = db.Column(db.String(64))



	# def get_api_token(self, expiration=300):
	# 	s = Serializer(current_app.config['SECRET_KEY'], expiration)
	# 	return s.dumps({'user': self.id}).decode('utf-8')
	#
	# @staticmethod
	# def validate_api(token):
	# 	s = Serializer(current_app.config['SECRET_KEY'])
	# 	try:
	# 		data = s.loads(token)
	# 	except:
	# 		return None
	# 	id = data.get('user')
	# 	if id:
	# 		return User.query.get(id)
	# 	return None
