#!/bin/bash -xe

python /usr/src/app/manage.py download_geolocation_data
python /usr/src/app/manage.py collectstatic --noinput
gunicorn conf.wsgi --bind [::1]:$PORT --bind 0.0.0.0:$PORT --log-file -
