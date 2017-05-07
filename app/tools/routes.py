import subprocess
import os
import requests
import json
import time
from luigi_tasks import Fib
from flask import render_template, current_app, request, redirect, url_for, flash, jsonify, Response, stream_with_context
from werkzeug import secure_filename
from ..tasks import fib, blast_task, upload_task
from flask_login import login_required, current_user
from . import tools
from .. import db, celery
from .forms import BlastForm, CawForm, UploadForm
from celery.result import AsyncResult


@tools.route('/luigi/fib/<int:n>')
def luigifib(n):
    # s = Fib(n)
    # s.run()
    subprocess.check_output(['luigi', '--module', 'luigi_tasks','Fib','--n',str(n),'--local-scheduler'])


@tools.route('/')
def index():
    return render_template('pages/index.html')


@tools.route('/blast', methods=['GET','POST'])
@login_required
def blast():
    form = BlastForm()
    if form.validate_on_submit():
        # Path to file: ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n') + '/' + form.fasta.data.filename
        fastafile = form.fasta.data
        filename = secure_filename(fastafile.filename)
        outfmt = form.outfmt.data
        blastn = form.blastAlgorithm.data
        evalue = form.evalue.data
        block = form.block_size.data

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
        # DO STUFF
        pass
        return redirect(url_for('tools.caw'))
    return render_template('tools/caw.html', form=form)

@tools.route('/filecontent')
def getfile():
    result = filecontent_thread()
    return result

@tools.route('/fib/<int:n>')
def fib_task(n):
    result = fib.apply_async(args=[n])
    flash('Fib %s running.' % str(result))
    task = Task(task_id=result.id, task_state=result.state, task_name='fib(%s)' % n)#, created_by=current_user)
    db.session.add(task)
    db.session.commit()
    return jsonify({'Check_results': url_for('tools.task_status', task_id=result), 'task_id': result.id, 'state': result.state})


@tools.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.filehandle.data
        filename = secure_filename(f.filename)
        save_data(filename)
        # result = upload_task.delay(path,filename,f)
        # f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))
        # result = upload_task(path,filename,f)
        flash("File Uploading")
        return redirect(url_for('pages.list_files'))
    return render_template('uploads/upload.html', form=form)


def stream_data(filename):
    with open(filename,'r') as f:
        for line in f:
            yield line


def save_data(filename):
    with open('userUploads/'+filename, 'w') as nf:
        for line in stream_data(filename):
            nf.write(line)
    return 'hi'

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

def filecontent_thread():
    from multiprocessing.pool import ThreadPool
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(fileContent,())
    return jsonify(async_result.get())

def fileContent():
    # fastafile = '/saves/newfa.fa'
    fastafile = ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n')+'/userUploads/newfa.fa'
    file_content = []
    with open(fastafile, 'r') as f:
        for n in range(500):
        # for line in f: # Entire file
            d = {'read_id':'', 'read': ''}
            d['read_id'] = f.readline().rstrip()
            d['read'] = f.readline().rstrip()
            file_content.append(d)
    return file_content
