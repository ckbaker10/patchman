FROM alpine:3.17 AS builder
# https://github.com/nimmis/docker-alpine/blob/master/Dockerfile
# I would have used his image but the versions are rather old

# ARG BUILD_DEPENDENCIES="build-base \
    # libffi-dev \
    # libxml2-dev \
    # mariadb-connector-c-dev \
    # openldap-dev \
    # python3-dev \
    # xmlsec-dev \
    # npm \
    # yarn \
    # cargo"
    
ARG BUILD_DEPENDENCIES="build-base \
    libffi-dev \
    libxml2-dev \
    mariadb-connector-c-dev \
    openldap-dev \
    python3-dev \
    xmlsec-dev \
    cargo"

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    FLASK_APP=/build/powerdnsadmin/__init__.py

RUN mkdir /tmp-pkg && cd /tmp-pkg && wget http://dl-cdn.alpinelinux.org/alpine/v3.17/main/x86_64/ca-certificates-20220614-r4.apk && apk add --allow-untrusted --no-network --no-cache /tmp-pkg/ca-certificates-20220614-r4.apk || true
RUN rm -rf /tmp/pkg
COPY ./docker/certs/certs.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates
COPY ./docker/certs/pip.conf /etc/


# Get dependencies
# py3-pip should not belong to BUILD_DEPENDENCIES. Otherwise, when we remove
# them with "apk del" at the end of build stage, the python requests module
# will be removed as well - (Tested with alpine:3.12 and python 3.8.5).
RUN apk add --no-cache ${BUILD_DEPENDENCIES} && \
    apk add --no-cache py3-pip

WORKDIR /build

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /build/
COPY ./requirementsDocker.txt /build/

# Get application dependencies
RUN pip install --upgrade pip && \
    pip install --use-pep517 -r requirements.txt &&\
    pip install --use-pep517 -r requirementsDocker.txt 

RUN apk add --no-cache redis


# Create Default sqlite path
RUN mkdir -p /var/lib/patchman/db

# Add sources
COPY . /build
COPY ./etc/patchman/local_settings_docker.py /build/etc/patchman/local_settings.py
COPY ./etc/patchman/local_settings_docker.py /etc/patchman/local_settings.py 

# Install Patchman Python locally for patchman -a
RUN python3 setup.py install

ENV PATCHMAN_SETTINGS_PATH "/build/etc/patchman"
ENV RUN_GUNICORN True
ENV PATCHMAN_DOCKER True
ENV BIND_ADDRESS 127.0.0.1:80


RUN chmod +x /build/docker/startup.sh

CMD ["sh", "-c", "docker/startup.sh" ]
