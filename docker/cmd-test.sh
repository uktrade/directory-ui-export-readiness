#!/bin/bash -xe

pip install -r requirements_test.txt --src /usr/local/src
python ./manage.py download_geolocation_data
make test
