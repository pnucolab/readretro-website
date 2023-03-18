from celery import Celery
import os

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_HOST = os.environ['POSTGRES_HOST']
POSTGRES_DB = os.environ['POSTGRES_DB']

celery_task = Celery(
    'app',
    broker="redis://{}:{}/0".format(os.environ.get('REDIS_HOST', '127.0.0.1'), os.environ.get('REDIS_PORT', '6379')),
    backend=f"db+postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:5432/{POSTGRES_DB}",
    include=['celery_worker']
)
