python manage.py migrate &&
python manage.py initializedb &&

python manage.py runserver 0.0.0.0:8000
#gunicorn --workers 3  --preload --bind 0.0.0.0:8000 djangoWeather.wsgi:application

