import subprocess
import os
import requests
import json
import time
import pykube
from flask import render_template, current_app, request, redirect, url_for, flash, jsonify, Response, stream_with_context
from werkzeug import secure_filename
from kubernetes import client, config
from ..tasks import fib, blast_task
from flask_login import login_required, current_user
from . import tools
from .. import db, celery
from ..models import Task
from .forms import BlastForm, CawForm, UploadForm, FibForm
from celery.result import AsyncResult

@tools.route('/')
def index():
    return render_template('pages/index.html')

@tools.route('/blast', methods=['GET','POST'])
@login_required
def blast():
    form = BlastForm()
    #TODO Fix stuff here
    if form.validate_on_submit():
        # Path to file: ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n') + '/' + form.fasta.data.filename
        fastafile = form.fasta.data
        filename = secure_filename(fastafile.filename)
        outfmt = form.outfmt.data
        blastn = form.blastAlgorithm.data
        evalue = form.evalue.data
        block = form.block_size.data

        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'],filename)

        result = blast_task.apply_async(args=[filename,outfmt,blastn,block,evalue])
        # result = blast_task.apply_async(args=[filename,outfmt,blastn,block,evalue])
        task = Task(task_id=result.id, task_state=result.state, task_name="Blast")
        db.session.add(task)
        db.session.commit()
        flash('Job running. Go to: "/tools/status/%s" to check job status.' % str(result))
        # addtodb(str(result), 'blast')
        return redirect(url_for('tools.blast'))
    return render_template('tools/blast.html', form=form)

@tools.route('/caw', methods=['GET', 'POST'])
def caw():
    form = CawForm()
    if form.validate_on_submit():
        #TODO DO STUFF
        pass
        return redirect(url_for('tools.caw'))
    return render_template('tools/caw.html', form=form)

@tools.route('/filecontent')
def getfile():
    result = filecontent_thread()
    return result

@tools.route('/fib', methods=['GET','POST'])
def fib_task():
    form = FibForm()
    if form.validate_on_submit():
        runFibTask = fib.apply_async(args=[form.number.data])
        flash('Fib %s running.' % str(runFibTask))
        task = Task(task_id=runFibTask.id, task_state=runFibTask.state, task_name='fib(%s)' % form.number.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('tools.fib_task'))
    return render_template('tools/fib.html', form=form)

@tools.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.filehandle.data
        filename = secure_filename(f.filename)
        save_data(filename)

        flash("File Uploading")
        return redirect(url_for('pages.list_files'))
    return render_template('uploads/upload.html', form=form)

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

def stream_data(filename):
    with open(filename,'r') as f:
        for line in f:
            yield line

def save_data(filename):
    with open('userUploads/'+filename, 'w') as nf:
        for line in stream_data(filename):
            nf.write(line)
    return 'hi'

def list_pods():
	client.Configuration().host = "http://localhost:8001"
	v1 = client.CoreV1Api()
	pod_list = v1.list_namespaced_pod("default")

	numPods = 0

	for pod in pod_list.items:
		if pod.status.phase == "Running":
			numPods += 1
	return numPods

def list_running_jobs():
    client.Configuration().host="http://localhost:8001"
    v1.client.BatchV1Api()
    job_list = v1.list_namespaced_job("default")

    return len(job_list)

def list_finished_jobs():
    client.Configuration().host="http://localhost:8001"
    v1.client.CoreV1Api()
    job_list = v1.list_namespaced_pod("default")

    finishedJobs = 0

    for job in job_list.items:
        if job.status.phase == "Succeeded":
            finishedJobs += 1

    return finishedJobs

def run_caw(data="/work/apps/pipeline_test/data/",name="cawcl",pdName="caw",memory="5Gi",cpu="2",threads="2"):
    api = pykube.HTTPClient(pykube.KubeConfig.from_url("http://localhost:8001"))

    obj = {
      "apiVersion": "batch/v1",
      "kind": "Job",
      "metadata": {
        "name": name
      },
      "spec": {
        "template": {
          "metadata": {
            "name": "caw"
          },
          "spec": {
            "volumes": [
              {
                "name": "myapp-persistent-job",
                "gcePersistentDisk": {
                  "pdName": pdName,
                  "fsType": "ext4"
                }
              }
            ],
            "containers": [
              {
                "name": "caw",
                "image": "firog/ubuntujava",
                "command": [
                  "bash",
                  "/work/apps/pipeline_test/flexible_location_pipeline.sh",
                  "/work/apps/pipeline_test/scratch/",
                  "/work/apps/",
                  "/work/apps/pipeline_test/ref/",
                  data,
                  threads
                ],
                "resources": {
                  "requests": {
                    "memory": memory,
                    "cpu": cpu
                  }
                },
                "volumeMounts": [
                  {
                    "name": "myapp-persistent-job",
                    "mountPath": "/work"
                  }
                ]
              }
            ],
            "restartPolicy": "Never"
          }
        }
      }
    }

    pykube.Job(api, obj).create()
