#!/bin/sh

python manage.py runserver --host 0.0.0.0
celery worker -A celery_worker.celery --loglevel=info
