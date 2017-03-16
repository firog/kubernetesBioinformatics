# Scalable

To run locally run: 
´´´bash
python manage.py runserver
´´´

Run celery worker(s):
´´´bash
celery worker -A celery_worker.celery --loglevel=info
´´´ 
