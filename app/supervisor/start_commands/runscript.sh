python /server/manage.py waitfordb &&
python /server/manage.py migrate &&
python /server/manage.py initializedb &&
# python /server/manage.py runserver 0.0.0.0:8000
gunicorn --workers 2 --bind 0.0.0.0:8000 app.wsgi:application

