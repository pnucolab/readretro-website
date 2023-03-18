celery -A celery_app worker -P gevent &
uvicorn main:app --host=0.0.0.0 --port=8000 --root-path /api/v1