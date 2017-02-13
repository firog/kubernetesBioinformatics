from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from ..models import User
from . import pages
from .forms import ProfileForm

@pages.route('/')
def index():
	return render_template('pages/index.html')

@pages.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	return render_template('pages/user.html', user=user)

@pages.route('/profile', methods=['GET','POST'])
@login_required
def profile():
	form = ProfileForm()
	if form.validate_on_submit():
		current_user.name = form.name.data
		current_user.location = form.location.data
		current_user.bio = form.bio.data
		db.session.add(current_user._get_current_object())
		db.session.commit()
		flash('Profile updated.')
		return redirect(url_for('pages.user', username=current_user.username))
	form.name.data = current_user.name
	form.location.data = current_user.location
	form.bio.data = current_user.bio
	return render_template('pages/profile.html', form=form)
