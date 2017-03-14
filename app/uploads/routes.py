from flask import render_template, flash, redirect, url_for, request, current_app
import os
import subprocess
from flask_login import login_required, current_user
from werkzeug import secure_filename
from .forms import UploadForm
from .. import db
from . import uploads

@uploads.route('/upload')
@login_required
def upload():
	return render_template('uploads/upload.html')

@uploads.route('/uploader', methods=['GET', 'POST'])
@login_required
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		filename = secure_filename(f.filename)
		f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
		flash('File uploaded, job will start when file has finished uploading.')
		subprocess.call(['makeblastdb','-in',filename,'-dbtype','nucl','-out',filename + "first"])
		subprocess.check_output(['blastn', '-db', filename+"first",'-query',filename+"first", '-evalue','1e-5','-num_threads','2'])
		return render_template('pages/index.html')

	# form = UploadForm()
	# if form.validate_on_submit():
	# 	f = form.uploadFile.data
	# 	filename = secure_filename(f.filename)
	# 	f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
	# 	return render_template('pages/index.html')
	# return render_template
