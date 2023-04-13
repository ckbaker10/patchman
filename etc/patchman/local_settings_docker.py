
DOCKER_VERBOSE_CONFIG = False
if os.environ.get('DOCKER_VERBOSE_CONFIG') is not None:
  DOCKER_VERBOSE_CONFIG = True

CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    'LOCATION': '127.0.0.1:11211',
  }
}
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': '/var/lib/patchman/db/patchman.db',
  }
}

if os.environ.get('PATCHMAN_DB') is "SQLLITE":
  SQLLITEPATH = '/var/lib/patchman/db/patchman.db'
  DATABASES = {
    'default': {
      'ENGINE': 'django.db.backends.sqlite3',
      'NAME': str(SQLLITEPATH),
    }
  }
else if os.environ.get('PATCHMAN_DB') is "POSTGRES":
  POSTGRES_USER = "patchman"
  POSTGRES_PASSWORD = "patchman"
  POSTGRES_DB = "patchman"
  POSTGRES_HOST = "127.0.0.1"
  POSTGRES_PORT = ""
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
  
if os.environ.get('PATCHMAN_CACHE') is "MEMCACHE":
  MEMCACHEPORT = '11211'
  MEMCACHEHOST = '127.0.0.1'
  CACHES = {
    'default': {
      'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
      'LOCATION': str(MEMCACHEHOST)+ ":"+str(MEMCACHEHOST),
    }
  }
else if os.environ.get('PATCHMAN_CACHE') is "REDIS":
  REDISHOST = "127.0.0.1"
  REDISPORT = 6379
  REDISDB = 1
  REDISAUTH = ""
  REDISKEYPREFIX = "patchman"
  
  CACHES = {
    "default": {
      "BACKEND": "django_redis.cache.RedisCache",
      "LOCATION": "redis://"+str(REDISHOST)+":"+str(REDISPORT)+"/"+str(REDISDB),
      "OPTIONS": {
        "PASSWORD": str(REDISAUTH),
        "CLIENT_CLASS": "django_redis.client.DefaultClient"
      },
      "KEY_PREFIX": str(REDISKEYPREFIX)
    }
  }

if DOCKER_VERBOSE_CONFIG:
    pp DATABASES
    pp CACHES

if os.environ.get('DEBUG') is not None:
  DEBUG = os.environ.get('DEBUG')
  if DOCKER_VERBOSE_CONFIG:
    pp DEBUG

if os.environ.get('PATCHMAN_SECRET_KEY') is not None:
  SECRET_KEY = str(os.environ.get('PATCHMAN_SECRET_KEY'))
  if DOCKER_VERBOSE_CONFIG:
    pp SECRET_KEY

if os.environ.get('TIME_ZONE') is not None:
  TIME_ZONE = os.environ.get('TIME_ZONE')
  if DOCKER_VERBOSE_CONFIG:
    pp TIME_ZONE
  
if os.environ.get('LANGUAGE_CODE') is not None:
  LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')
  if DOCKER_VERBOSE_CONFIG:
    pp LANGUAGE_CODE

if os.environ.get('PATCHMAN_MAX_MIRRORS') is not None:
  MAX_MIRRORS = os.environ.get('PATCHMAN_MAX_MIRRORS')
  if DOCKER_VERBOSE_CONFIG:
    pp MAX_MIRRORS
  
if os.environ.get('PATCHMAN_DAYS_WITHOUT_REPORT') is not None:
  DAYS_WITHOUT_REPORT = os.environ.get('PATCHMAN_DAYS_WITHOUT_REPORT')
  if DOCKER_VERBOSE_CONFIG:
    pp DAYS_WITHOUT_REPORT

  
if os.environ.get('RUN_GUNICORN') is not None:
  RUN_GUNICORN = (os.environ.get('RUN_GUNICORN') == "True")
  if DOCKER_VERBOSE_CONFIG:
    pp RUN_GUNICORN