from flask import render_template
from ..models import User
from . import pages

@pages.route('/')
def index():
	return render_template('pages/index.html')

@pages.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('pages/user.html', user=user)
