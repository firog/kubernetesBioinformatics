import subprocess
import os
import requests
import json
from flask import render_template, current_app, request, redirect, url_for, flash, jsonify
from werkzeug import secure_filename
from ..tasks import fib, blast_task, wherami, test_uptask
from ..models import Task
from flask_login import login_required, current_user
from . import tools
from .. import db, celery
from .forms import BlastForm, CawForm, UploadForm
from libcloud.storage.types import Provider
from libcloud.storage.providers import get_driver
from celery.result import AsyncResult

@tools.route('/')
def index():
    return render_template('pages/index.html')

@tools.route('/results')
def results():
    pass

@tools.route('/blast', methods=['GET','POST'])
@login_required
def blast():
    form = BlastForm()
    if form.cloud_provider.data == 'GCE':
        # clsp = get_driver(Provider.GOOGLE_STORAGE)
        pass #TODO add apache libcloud support for GCE

    elif form.cloud_provider.data == 'AWS':
        pass #TODO add apache libcloud support for AWS

    elif form.cloud_provider.data == 'Azure':
        pass #TODO add apache libcloud support for Azure

    if form.validate_on_submit():
        # Path to file: ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n') + '/' + form.fasta.data.filename
        fastafile = form.fasta.data
        filename = secure_filename(fastafile.filename)
        outfmt = form.outfmt.data
        blastn = form.blastAlgorithm.data
        block = form.block_size.data
        evalue = form.evalue.data

        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)
        # result = chord(upload_task.s(fastafile,save_path), blast_task.s(filename,outfmt,blastn,block,evalue))
        # result = upload_task.apply_async(args=[fastafile,save_path])

        # resultUpload = upload_task(fastafile,save_path)
        result = blast_task.apply_async(args=[filename,outfmt,blastn,block,evalue])
        # result = blast_task.apply_async(args=[filename,outfmt,blastn,block,evalue])

        flash('Job running. Go to: "/tools/status/%s" to check job status.' % str(result))
        addtodb(str(result), 'blast')
        return redirect(url_for('tools.blast'))
    return render_template('tools/blast.html', form=form)


@tools.route('/caw', methods=['GET', 'POST'])
def caw():
    form = CawForm()
    if form.validate_on_submit():
        f = form.zipfile.data
        result = test_uptask.apply_async(args=[f])
        flash('Check results: /tools/status/%s' % str(result))
        addtodb(str(result), 'caw')
        return redirect(url_for('tools.caw'))
    return render_template('tools/caw.html', form=form)


@tools.route('/wherami')
def wherami_task():
    task = wherami.apply_async()
    jsonformat = jsonify({'path':str(task.get())})
    return task.get()


@tools.route('/fib/<int:n>')
def fib_task(n):
    result = fib.apply_async(args=[n])
    flash('Fib %s running.' % str(result))
    # addtodb(result.id, task_name)
    task = Task(task_id=result.id, task_state=result.state, task_name='fib(%s)' % n)#, created_by=current_user)
    db.session.add(task)
    db.session.commit()
    return jsonify({'Check_results': url_for('tools.task_status', task_id=result), 'task_id': result.id, 'state': result.state})

@tools.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['files']
        filename = secure_filename(f.filename)
        f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return '200'
    return '405'

@tools.route('/files')
def list_files():
    filelst = os.listdir(os.path.join(current_app.config['UPLOAD_FOLDER']))
    filedic = {}
    filedic['files'] = filelst
    data = jsonify(filedic)
    return render_template('tools/list_files.html', data=filedic)

@tools.route('/jobs')
def list_jobs():
    pass

@tools.route('/status/<task_id>')
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
        'state': task.state,
        'status': 'Pending...'
        }
        return jsonify(response)
    else:
        # return jsonify({'state': task.state, 'result': str(task.get())})
        return jsonify({'result': str(task.get())})

@tools.route('/raxml')
@login_required
def raxml():
    return render_template("tools/raxml.html")


@tools.route('/othertool')
@login_required
def othertool():
    return render_template("tools/othertool.html")


def addtodb(task_id,task_name):
    task = Task(task_id=str(task_id), task_state=get_state(task_id), task_name=task_name)#, created_by=current_user)
    db.session.add(task)
    db.session.commit()

def test_up(f):
    filename = secure_filename(f.filename)
    f.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
    return '200'

def get_state(task_id):
    pass
    # task = AsyncResult(task_id)
    # return task.state

def task_update(task_id):
    status = celery.AsyncResult(task_id)
    task = Task.query.filter(Task.task_id == task_id).one()
    if status.state == 'SUCCESS':
        task.result = status.get()
        task.task_state = status.state
    else:
        task.result = 'Not ready'
        task.task_state = status.state
    db.session.add(task)
    db.session.commit()
    # if Task.query.filter_by(task_id = task_id).first() is None:
    #     abort(400, "Task id does not exist")
    # task = Task.query.filter(Task.task_id == task_id).one()
    # task.task_state = get_state(task_id)
    # db.session.add(task)
    # db.session.commit()
