from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from .. import db
from ..models import User, Post
from . import pages
from .forms import ProfileForm, PostForm

@pages.route('/')
@pages.route('/home')
def index():
	post_list = Post.query.order_by(Post.date.desc()).all()
	return render_template('pages/index.html', posts=post_list)

@pages.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	post_list = user.posts.order_by(Post.date.desc()).all()
	return render_template('pages/user.html', user=user, posts=post_list)


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
# @login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash("Posted!")
		return redirect(url_for('.index'))
	return render_template('pages/edit_post.html', form=form)


@pages.route('/post/<int:id>')
def post(id):
	post = Post.query.get_or_404(id)
	return render_template('pages/post.html', post=post)
