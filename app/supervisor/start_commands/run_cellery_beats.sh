python /server/manage.py waitfordb &&
celery -A app beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler