celery -A PinguBackend  worker --loglevel=info -E &

celery -A PinguBackend beat  --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler