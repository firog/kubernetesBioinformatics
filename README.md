# Scalable cloud community

`git clone https://github.com/firog/scalableCloudCommunity.git`

`pip install -r requirements.txt`

To run locally run: `python manage.py runserver`

Run celery worker(s): `celery worker -A celery_worker.celery --loglevel=info`

