FROM alpine:3.17 AS builder

ARG BUILD_DEPENDENCIES="build-base \
    libffi-dev \
    libxml2-dev \
    mariadb-connector-c-dev \
    openldap-dev \
    python3-dev \
    xmlsec-dev \
    npm \
    yarn \
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

# Add sources
COPY . /build

ENV PATCHMAN_SETTINGS_PATH "./etc/patchman"

# Prepare assets
#RUN yarn install --pure-lockfile --production 
#RUN yarn cache clean 
#RUN sed -i -r -e "s|'cssmin',\s?'cssrewrite'|'rcssmin'|g" /build/powerdnsadmin/assets.py
##RUN sed -i -r -e "s|'cssmin',\s?'cssrewrite'|'cssmin'|g" /build/powerdnsadmin/assets.py
#RUN flask assets build

#RUN mv /build/powerdnsadmin/static /tmp/static && \
#    mkdir /build/powerdnsadmin/static && \
#    cp -r /tmp/static/generated /build/powerdnsadmin/static && \
#    cp -r /tmp/static/assets /build/powerdnsadmin/static && \
#    cp -r /tmp/static/img /build/powerdnsadmin/static && \
#    find /tmp/static/node_modules -name 'webfonts' -exec cp -r {} /build/powerdnsadmin/static \; && \
#    find /tmp/static/node_modules -name 'fonts' -exec cp -r {} /build/powerdnsadmin/static \; && \
#    find /tmp/static/node_modules/icheck/skins/square -name '*.png' -exec cp {} /build/powerdnsadmin/static/generated \;

#RUN { \
#      echo "from flask_assets import Environment"; \
#      echo "assets = Environment()"; \
#      echo "assets.register('js_login', 'generated/login.js')"; \
#      echo "assets.register('js_validation', 'generated/validation.js')"; \
#      echo "assets.register('css_login', 'generated/login.css')"; \
#      echo "assets.register('js_main', 'generated/main.js')"; \
#      echo "assets.register('css_main', 'generated/main.css')"; \
#    } > /build/powerdnsadmin/assets.py

# Move application
#RUN mkdir -p /app && \
#    cp -r /build/migrations/ /build/powerdnsadmin/ /build/run.py /app && \
#    mkdir -p /app/configs && \
#    cp -r /build/configs/docker_config.py /app/configs

CMD ["gunicorn", "patchman.wsgi", "-b", "0.0.0.0:80" ]
