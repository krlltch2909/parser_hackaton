python /server/manage.py waitfordb &&
celery -A app worker -l INFO