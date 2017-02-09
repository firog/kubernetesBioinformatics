from flask import Flask, render_template
from celery import Celery
from tasks import reverse, add

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='amqp://localhost//',
    CELERY_RESULT_BACKEND='amqp://'
)
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@app.route('/')
@app.route('/index')
def index():
	return render_template('base.html')

@app.route('/process/add/<int:x>+<int:y>')
def proAdd(x,y):
	add.delay(x,y)
	return "sent Async"

@app.route('/process/<name>')
def process(name):
	s = reverse.delay(name)
	return s.wait()

if __name__ == '__main__':
	app.run(debug=True)
