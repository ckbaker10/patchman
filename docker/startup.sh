#!/bin/sh
python3 /build/manage.py makemigrations
python3 /build/manage.py migrate --run-syncdb

UNQUOTED_BIND_ADDRESS=$(echo $BIND_ADDRESS | xargs)
gunicorn patchman.wsgi -b $UNQUOTED_BIND_ADDRESS