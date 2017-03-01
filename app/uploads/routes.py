from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug import secure_filename
from .. import db
from . import uploads
# from .forms import UploadForm

@uploads.route('/upload')
@login_required
def upload():
	return render_template('uploads/upload.html')

# @pages.route('/tools/blast')
# @login_required
# def blast_view():
# 	return render_template('pages/blast.html')

@uploads.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		flash('File uploaded, job will start when file has finished uploading.')
		return render_template('pages/index.html')
