import os
from flask import render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user
from .. import db
from ..models import User, Post, Task
from app.tools.routes import task_update, list_pods
from api_1_0.endpoints.task import TaskList
from . import pages
from .forms import ProfileForm, PostForm

@pages.route('/')
@pages.route('/home')
def index():
	post_list = Post.query.order_by(Post.date.desc()).all()
	job_list = Task.query.all()
	numPods = list_pods()
	return render_template('pages/index.html', postsLength=len(post_list), jobLength=len(job_list), numPods=numPods)

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
@login_required
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

@pages.route('/files')
def list_files():
	filelst = os.listdir(os.path.join(current_app.config['UPLOAD_FOLDER']))
	filedic = {}
	filedic['files'] = filelst
	data = jsonify(filedic)
	return render_template('pages/list_files.html', data=filedic)

@pages.route('/jobs')
def list_jobs():
	tasklst = Task.query.all()
	for task in tasklst:
		if task.task_state != 'SUCCESS':
			task_update(task.task_id)
	return render_template('pages/list_jobs.html', data=tasklst)

@pages.route('/posts')
def list_posts():
	posts = Post.query.all()
	return render_template('pages/list_posts.html',data=posts)
