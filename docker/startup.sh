#!/bin/sh
python3 /build/manage.py makemigrations
python3 /build/manage.py migrate --run-syncdb