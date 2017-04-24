from flask import request
from werkzeug import secure_filename
from . import celery
from app import config
import subprocess
import os
import asyncio

@celery.task
def fib(n):
    if n==1 or n==2:
        return 1
    return fib(n-1)+fib(n-2)

@asyncio.coroutine
def upload_task(path, filename,f):
    with open(path+'/'+filename, 'wa') as fe:
        file_content = yield from load_file(f)
        print(file_content)
    # f.save(os.path.join(current_app.config['UPLOAD_FOLDER'],filename))



@celery.task
def blast_task(filename,outfmt,blastn,block,evalue):
    wherami = ((subprocess.check_output(["pwd"])).decode('UTF-8')).rstrip('\n')
    scripts_path = wherami+'bashscripts'
    filename = wherami+'/userUploads/newfa.fa'
    subprocess.call(['/myapp/makeblastdb','-in',filename,'-dbtype','nucl','-out',filename+'db'])
    subprocess.call(['%s/bashscripts/runparallelblast.sh' % wherami ,filename, block, "/myapp/"+blastn, evalue, outfmt, filename+'db'])


@celery.task
def caw_task():
    pass
