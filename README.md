# Scalable cloud community

`git clone https://github.com/firog/scalableCloudCommunity.git`

`pip install -r requirements.txt`

To run locally run: `python manage.py runserver`

Run celery worker(s): `celery worker -A celery_worker.celery --broker=amqp://guest:guest@localhost:5672// --loglevel=info`


To use Kubernetes, first create a cluster in GCE and configure kubectl for that cluster.

Run: `./createcluster.sh` 
