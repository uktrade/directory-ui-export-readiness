web: python manage.py download_geolocation_data && python manage.py collectstatic --noinput && gunicorn ui.wsgi --bind 0.0.0.0:$PORT
