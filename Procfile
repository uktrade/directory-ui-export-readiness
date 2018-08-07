web: python manage.py download_geolocation_data && python manage.py collectstatic --noinput && gunicorn conf.wsgi --bind 0.0.0.0:$PORT
