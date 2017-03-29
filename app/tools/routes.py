import subprocess
import os
import json
from flask import render_template, current_app, request, redirect, url_for, flash, jsonify
from werkzeug import secure_filename
from celery import chord
from time import time
from ..tasks import fib, blast_task, wherami, upload_task
from flask_login import login_user, logout_user, login_required
from . import tools
from .forms import BlastForm

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
        from libcloud.storage.types import Provider
        from libcloud.storage.providers import get_driver

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

        flash('Job running. Go to: "localhost:5000/tools/status/%s" to check job status.' % str(result))
        return redirect(url_for('tools.blast'))
    return render_template('tools/blast.html', form=form)


@tools.route('/wherami')
def wherami_task():
    task = wherami.apply_async()
    jsonformat = jsonify({'path':str(task.get())})
    return task.get()+'/test'


@tools.route('/fib/<int:n>')
def fib_task(n):
    result = fib.apply_async(args=[n])
    flash('Fib %s running.' % str(result))
    return jsonify({'task_id': str(result), 'state': result.state, \
        'check_result': 'localhost:5000/tools/status/' + str(result) })

@tools.route('/status/<task_id>')
def task_status(task_id):
    task = fib.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
        'state': task.state,
        'status': 'Pending...'
        }
        return jsonify(response)
    else:
        return jsonify({'state': task.state, 'result': str(task.get())})

@tools.route('/raxml')
@login_required
def raxml():
    return render_template("tools/raxml.html")


@tools.route('/othertool')
@login_required
def othertool():
    return render_template("tools/othertool.html")
