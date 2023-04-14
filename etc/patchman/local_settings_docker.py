import pprint
import os
pp = pprint.PrettyPrinter(indent=2)

DOCKER_VERBOSE_CONFIG = False
if os.environ.get('DOCKER_VERBOSE_CONFIG') is not None:
  DOCKER_VERBOSE_CONFIG = True

# Default Values
# Using Internal Redis by Default
CACHES = {
    "default": {
      "BACKEND": "django_redis.cache.RedisCache",
      "LOCATION": "redis://127.0.0.1:6379/1",
      "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient"
      },
      "KEY_PREFIX": "PATCHMAN"
    }
  }
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '/var/lib/patchman/db/patchman.db',
  }
}

DEBUG=False

CELERY_BROKER_URL="redis://127.0.0.1:6379/0"

USE_ASYNC_PROCESSING = True

if os.environ.get('PATCHMAN_DB') == "SQLLITE":
  SQLLITEPATH = '/var/lib/patchman/db/patchman.db'
  if os.environ.get('SQLLITEPATH') is not None:
    SQLLITEPATH = str(os.environ.get('SQLLITEPATH'))
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': str(SQLLITEPATH),
    }
  }
elif os.environ.get('PATCHMAN_DB') == "POSTGRES":
  POSTGRES_USER = "patchman"
  POSTGRES_PASSWORD = "patchman"
  POSTGRES_DB = "patchman"
  POSTGRES_HOST = "127.0.0.1"
  POSTGRES_PORT = ""
  if os.environ.get('POSTGRES_USER') is not None:
    POSTGRES_USER = str(os.environ.get('POSTGRES_USER'))
  if os.environ.get('POSTGRES_PASSWORD') is not None:
    POSTGRES_PASSWORD = str(os.environ.get('POSTGRES_PASSWORD'))
  if os.environ.get('POSTGRES_DB') is not None:
    POSTGRES_DB = str(os.environ.get('POSTGRES_DB'))
  if os.environ.get('POSTGRES_HOST') is not None:
    POSTGRES_HOST = str(os.environ.get('POSTGRES_HOST'))
  if os.environ.get('POSTGRES_PORT') is not None:
    POSTGRES_PORT = str(os.environ.get('POSTGRES_PORT'))
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.postgresql_psycopg2',
      'NAME': str(POSTGRES_DB),
      'USER': str(POSTGRES_USER),
      'PASSWORD': str(POSTGRES_PASSWORD),
      'HOST': str(POSTGRES_HOST),
      'PORT': str(POSTGRES_PORT),
      'CHARSET' : 'utf8'
    }
  }
  
if os.environ.get('PATCHMAN_CACHE') == "MEMCACHE":
  MEMCACHEPORT = '11211'
  MEMCACHEHOST = '127.0.0.1'
  if os.environ.get('MEMCACHEPORT') is not None:
    MEMCACHEPORT = str(os.environ.get('MEMCACHEPORT'))
  if os.environ.get('MEMCACHEHOST') is not None:
    MEMCACHEHOST = str(os.environ.get('MEMCACHEHOST'))
  CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
      'LOCATION': str(MEMCACHEHOST) + ":" + str(MEMCACHEHOST),
    }
  }
elif os.environ.get('PATCHMAN_CACHE') == "REDIS":
  REDISHOST = "127.0.0.1"
  REDISPORT = 6379
  REDISDB = 1
  REDISAUTH = ""
  REDISKEYPREFIX = "PATCHMAN"
  if os.environ.get('REDISHOST') is not None:
    REDISHOST = str(os.environ.get('REDISHOST'))
  if os.environ.get('REDISPORT') is not None:
    REDISPORT = str(os.environ.get('REDISPORT'))
  if os.environ.get('REDISDB') is not None:
    REDISDB = str(os.environ.get('REDISDB'))
  if os.environ.get('REDISAUTH') is not None:
    REDISAUTH = str(os.environ.get('REDISAUTH'))
  if os.environ.get('REDISKEYPREFIX') is not None:
    REDISKEYPREFIX = str(os.environ.get('REDISKEYPREFIX'))
  
  CACHES = {
    "default": {
      "BACKEND": "django_redis.cache.RedisCache",
      "LOCATION": "redis://" + str(REDISHOST) + ":" + str(REDISPORT) + "/" + str(REDISDB),
      "OPTIONS": {
        "PASSWORD": str(REDISAUTH),
        "CLIENT_CLASS": "django_redis.client.DefaultClient"
      },
      "KEY_PREFIX": str(REDISKEYPREFIX)
    }
  }

  
  #CELERY_BROKER_URL = "redis://:" + str(REDISAUTH) + "@" + str(REDISHOST) + ":" + str(REDISPORT) + "/0"
  # Using an Internal REDIS

if DOCKER_VERBOSE_CONFIG:
  print("-------------PARSED DOCKER ENVIRONMENT VARIABLES-------------")
  print("DATABASES")
  pp.pprint(DATABASES)
  print("CACHES")
  pp.pprint(CACHES)

if os.environ.get('DEBUG') is not None:
  DEBUG = os.environ.get('DEBUG')
  if DOCKER_VERBOSE_CONFIG:
    print("DEBUG")
    pp.pprint(DEBUG)

if os.environ.get('PATCHMAN_SECRET_KEY') is not None:
  SECRET_KEY = str(os.environ.get('PATCHMAN_SECRET_KEY'))
  if DOCKER_VERBOSE_CONFIG:
    print("SECRET_KEY")
    pp.pprint(SECRET_KEY)

if os.environ.get('TIME_ZONE') is not None:
  TIME_ZONE = os.environ.get('TIME_ZONE')
  if DOCKER_VERBOSE_CONFIG:
    print("TIME_ZONE")
    pp.pprint(TIME_ZONE)
  
if os.environ.get('LANGUAGE_CODE') is not None:
  LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
  if DOCKER_VERBOSE_CONFIG:
    print("LANGUAGE_CODE")
    pp.pprint(LANGUAGE_CODE)

if os.environ.get('PATCHMAN_MAX_MIRRORS') is not None:
  MAX_MIRRORS = os.environ.get('PATCHMAN_MAX_MIRRORS')
  if DOCKER_VERBOSE_CONFIG:
    print("MAX_MIRRORS")
    pp.pprint(MAX_MIRRORS)
  
if os.environ.get('PATCHMAN_DAYS_WITHOUT_REPORT') is not None:
  DAYS_WITHOUT_REPORT = os.environ.get('PATCHMAN_DAYS_WITHOUT_REPORT')
  if DOCKER_VERBOSE_CONFIG:
    print("DAYS_WITHOUT_REPORT")
    pp.pprint(DAYS_WITHOUT_REPORT)
  
if os.environ.get('RUN_GUNICORN') is not None:
  RUN_GUNICORN = (os.environ.get('RUN_GUNICORN') == "True")
  if DOCKER_VERBOSE_CONFIG:
    print("RUN_GUNICORN")
    pp.pprint(RUN_GUNICORN)

if DOCKER_VERBOSE_CONFIG:
  print("USE_ASYNC_PROCESSING")
  pp.pprint(USE_ASYNC_PROCESSING)

if DOCKER_VERBOSE_CONFIG:
  print("CELERY_BROKER_URL")
  pp.pprint(CELERY_BROKER_URL)

  
if DOCKER_VERBOSE_CONFIG:
  print("-------------------------------------------------------------")