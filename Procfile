web: python manage.py collectstatic --noinput && python manage.py compilemessages && gunicorn ui.wsgi --bind 0.0.0.0:$PORT
