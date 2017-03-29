# Scalable cloud community
To run locally:
`git clone https://github.com/firog/scalableCloudCommunity.git`

`pip install -r requirements.txt`

`python manage.py runserver`

Run celery worker(s): `celery worker -A celery_worker.celery --broker=amqp://guest:guest@localhost:5672// --loglevel=info`

To run on a cloud provider using Kubernetes:

First create a cluster on GCE, AWS or Azure and configure kubectl for that cluster.

cd into kubeSpec and Run: `./createcluster.sh`
