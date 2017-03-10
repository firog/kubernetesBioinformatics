import re
from flask_restplus import abort
from flask import jsonify
from app import db
from app.models import User

email_regex = re.compile(
    r'^'
    '(?P<local>[^@]*[^@.])'
    r'@'
    r'(?P<server>[^@]+(?:\.[^@]+)*)'
    r'$', re.IGNORECASE)

def get_user(username):
    if User.query.filter_by(username = username).first() is None:
        abort(400, "User does not exist")
    return User.query.filter(User.username == username).one()

def update_user(username, data):
    if User.query.filter_by(username = data.get('username')).first() is None:
        abort(400, "User does not exist")
    user = User.query.filter(User.username == username).one()
    user.username = data.get('username')
    user.name = data.get('name')
    user.is_admin = data.get('is_admin')
    db.session.add(user)
    db.session.commit()

def create_user(data):
    # if email_regex.match(data.get('email')):
    user = User(email=data.get('email'),username=data.get('username'), \
                password=data.get('password'), \
                is_admin=data.get('is_admin'), name=data.get('name'))
    if User.query.filter_by(username = data.get('username')).first() is not None:
        abort(400, "User exists")
    if data.get('username') is None or data.get('password') is None:
        abort(400, "Missing parameters")
    db.session.add(user)
    db.session.commit()
    return jsonify({'username': data.get('username')})

def delete_user(username):
    if User.query.filter_by(username = username).first() is None:
        abort(400, "User does not exist")
    user = User.query.filter(User.username == username).one()
    db.session.delete(user)
    db.session.commit()
