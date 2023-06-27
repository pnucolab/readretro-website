celery -A celery_app worker --loglevel=INFO &
uvicorn main:app --host=0.0.0.0 --port=8000 --root-path /api/v1 --proxy-headers --forwarded-allow-ips '*'
