# Scalable cloud community

`git clone https://github.com/firog/scalableCloudCommunity.git`

`pip install -r requirements.txt`

To run locally run: `python manage.py runserver`

Run celery worker(s): `celery worker -A celery_worker.celery --broker=amqp://guest:guest@localhost:5672// --loglevel=info`


To use Kubernetes, first create a cluster on GCE, AWS or Azure and configure kubectl for that cluster.

cd into kubeSpec and Run: `./createcluster.sh`
