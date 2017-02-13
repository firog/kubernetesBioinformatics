from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from .. import db
from ..models import User, ForumTopic
from . import pages
from .forms import ProfileForm, CreateThreadForm

@pages.route('/')
def index():
	posts = ForumTopic.query.order_by(ForumTopic.date.desc()).all()
	return render_template('pages/index.html', post=posts)

@pages.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = user.fThread.order_by(ForumTopic.date.desc()).all()
	return render_template('pages/user.html', user=user, post=posts)

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

@pages.route('/new', methods=['GET','POST'])
@login_required
def new_post():
    form = CreateThreadForm()
    if form.validate_on_submit():
        post = ForumTopic(topicTitle=form.topicTitle.data,
        content=form.content.data,
        author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Posted!")
        return redirect(url_for('.index'))
    return render_template('pages/edit_post.html', form=form)
