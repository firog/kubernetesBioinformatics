from flask import render_template, current_app, request, redirect, url_for, flash, jsonify, Markup
import json
from werkzeug import secure_filename
from time import time
from ..tasks import fib, blast_task, wherami
import subprocess
import os
from flask_login import login_user, logout_user, login_required
from . import tools
from .forms import BlastForm, AddForm

@tools.route('/')
def index():
    return render_template('pages/index.html')

@tools.route('/blast', methods=['GET','POST'])
@login_required
def blast():
    form = BlastForm()
    if form.validate_on_submit():
        fastafile = form.filename.data
        filename = secure_filename(fastafile.filename)
        outfmt = form.outfmt.data
        blastn = form.blastAlgorithm.data
        block = form.block_size.data
        evalue = form.evalue.data
        result = blast_task.apply_async(args=[filename,outfmt,blastn,block,evalue])
        # flash(Markup('Job running. Go to:<a href="localhost:5000/tools/status/%s" class="alert-link">here</a>.'% str(result)))
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
