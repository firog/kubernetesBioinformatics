from celery import Celery
import subprocess

app = Celery('tasks', backend='amqp://', broker='amqp://')

@app.task
def reverse(string):
	return string[::-1]

@app.task
def add(x,y):
	return x+y

@app.task
def formatBlastdb(infile):
	pass
