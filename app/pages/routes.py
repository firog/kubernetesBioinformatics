from flask import render_template
from . import pages

@pages.route('/')
def index():
	return render_template('pages/index.html')

@pages.route('/user/<username>')
def user(username):
	return render_template('pages/user.html', username=username)


