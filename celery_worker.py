#!/usr/bin/env python
import os
from app import celery, create_app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
# app.config['CELERY_BROKER_URL'] = os.environ.get('RABBITMQ_SERVICE_SERVICE_HOST')
app.app_context().push()
