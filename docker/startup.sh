#!/bin/sh
FILEPATH=$(readlink -f "$0");
SCRIPTPATH=$(dirname "$FILEPATH");
cd "$SCRIPTPATH"
python3 /build/manage.py makemigrations
python3 /build/manage.py migrate --run-syncdb

if [ -d ./certs ]; then
  if ls ./certs/*.crt 1> /dev/null 2>&1; then
    rm -rf /usr/local/share/ca-certificates/*
    update-ca-certificates
    cat ./certs/custom/*.crt >> /etc/ssl/certs/ca-certificates.crt
    # openssl s_client -showcerts -servername packages.rundeck.com -connect packages.rundeck.com:443
    
    #if [ ! -f /usr/lib/python3.10/site-packages/certifi/cacert.pem.orig ]; then
    #  cp /usr/lib/python3.10/site-packages/certifi/cacert.pem /usr/lib/python3.10/site-packages/certifi/cacert.pem.orig
    #fi
    # Restore original content first if we are restarting here
    ## cat /usr/lib/python3.10/site-packages/certifi/cacert.pem.orig > /usr/lib/python3.10/site-packages/certifi/cacert.pem
    # Add custom certs to certifi truststore
    # https://stackoverflow.com/a/57910133
    ##cat ./certs/*.crt >> /usr/lib/python3.10/site-packages/certifi/cacert.pem
    cat <<\EOF > /etc/pip.conf
[global]
cert = /etc/ssl/certs/ca-certificates.crt
EOF
  fi
fi


cp /etc/ssl/certs/ca-certificates.crt /usr/lib/python3.10/site-packages/certifi/cacert.pem

UNQUOTED_BIND_ADDRESS=$(echo $BIND_ADDRESS | xargs)
gunicorn patchman.wsgi -b $UNQUOTED_BIND_ADDRESS