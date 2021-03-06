from flask import render_template, current_app, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import User
from . import auth
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
	if not current_app.config['DEBUG'] and not current_app.config['TESTING'] and not request.is_secure:
		return redirect(url_for('.login', _external=True, _scheme='https'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None or not user.verify_password(form.password.data):
			flash('Invalid username or password.')
			return redirect(url_for('.login'))
		login_user(user, form.remember_me.data)
		return redirect(request.args.get('next') or url_for('pages.index'))
	return render_template('auth/login.html', form=form)


# @auth.route('/login', methods=['GET', 'POST'])
# def login():
# 	if request.method == 'POST':
# 		form = LoginForm(request.form)
# 		if form.validate():
# 			user = User.query.filter_by(email=form.email.data).first()
# 			if user is None or not user.verify_password(form.password.data):
# 				flash('Invalid username or password.')
# 				return redirect(url_for('.login'))
# 			login_user(user, form.remember_me.data)
# 			return redirect(url_for('pages.index'))
# 		return render_template('auth/login.html', form=LoginForm())
# 	# 	else:
# 	# 		return render_template('auth/login.html', form=form)
# 	return render_template('auth/login.html', form=LoginForm())

@auth.route('/logout')
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('pages.index'))
