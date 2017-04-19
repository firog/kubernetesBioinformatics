from flask import request
from werkzeug import secure_filename
from . import celery
from app import config
import subprocess
import os

@celery.task
def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1)+fib(n-2)

@celery.task
def wherami():
    return ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n')


@celery.task
def blast_task(filename,outfmt,blastn,block,evalue):
    wherami = ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n')
    scripts_path = wherami+'bashscripts'

    # filename.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    filename = wherami+'/userUploads/newfa.fa'
    subprocess.call(['/myapp/makeblastdb','-in',filename,'-dbtype','nucl','-out',filename+'db'])
    subprocess.call(['%s/bashscripts/runparallelblast.sh' % wherami ,filename, block, "/myapp/"+blastn, evalue, outfmt, filename+'db'])


@celery.task
def test_uptask(f):
    filename = secure_filename(f.filename)
    f.save('/saves',filename)
    # f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return '200'


@celery.task(ignore_result=True)
def upload_task(dataFile, save_path):
    # dataFile.save(save_path)
    # filename.save(save_path)

    # form = UploadForm()
	# if form.validate_on_submit():
	# 	f = form.uploadFile.data
	# 	filename = secure_filename(f.filename)
	# 	f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
	# 	return render_template('pages/index.html')
	# return render_template

    pass
    # f = request.files['file']
    # filename = secure
    #
    #
    #
    # 		return render_template('pages/index.html')
