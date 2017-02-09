from celery import Celery

app = Celery('tasks', broker='amqp://', backend='amqp://')

@app.tasks
def mname(self, arg):
    pass
