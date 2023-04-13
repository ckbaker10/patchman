#!/bin/sh
FILEPATH=$(readlink -f "$0");
SCRIPTPATH=$(dirname "$FILEPATH");
cd "$SCRIPTPATH"
python3 /build/manage.py makemigrations
python3 /build/manage.py migrate --run-syncdb

if [ -f ./certs ]; then
  if ls ./certs/*.crt 1> /dev/null 2>&1; then
    cp ./certs/custom/*.crt /usr/local/share/ca-certificates/
    update-ca-certificates
    cat ./certs/*.crt > /usr/local/share/ca-certificates/certs.crt
    cat <<\EOF > /etc/pip.conf
[global]
cert = /usr/local/share/ca-certificates/certs.crt
EOF
  fi
fi

UNQUOTED_BIND_ADDRESS=$(echo $BIND_ADDRESS | xargs)
gunicorn patchman.wsgi -b $UNQUOTED_BIND_ADDRESS