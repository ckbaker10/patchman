
CACHES = { }
DATABASES = { }

if os.environ.get('PATCHMAN_DB_SQLLITE') is not None:
  SQLLITEPATH = '/var/lib/patchman/db/patchman.db'
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.sqlite3',
          'NAME': '/var/lib/patchman/db/patchman.db',
      }
  }
  
if os.environ.get('DEBUG') is not None:
  DEBUG = os.environ.get('DEBUG')

if os.environ.get('PATCHMAN_SECRET_KEY') is not None:
  SECRET_KEY = os.environ.get('SECRET_KEY')

if os.environ.get('TIME_ZONE') is not None:
  TIME_ZONE = os.environ.get('TIME_ZONE')
  
if os.environ.get('LANGUAGE_CODE') is not None:
  LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE')

if os.environ.get('PATCHMAN_MAX_MIRRORS') is not None:
  MAX_MIRRORS = os.environ.get('MAX_MIRRORS')
  
if os.environ.get('PATCHMAN_DAYS_WITHOUT_REPORT') is not None:
  DAYS_WITHOUT_REPORT = os.environ.get('DAYS_WITHOUT_REPORT')

if os.environ.get('PATCHMAN_CACHE_MEMCACHE') is not None:
  MEMCACHEPORT = '11211'
  MEMCACHEHOST = '127.0.0.1'
  CACHES = {
      'default': {
          'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
          'LOCATION': '127.0.0.1:11211',
      }
  }
  
if os.environ.get('RUN_GUNICORN') is not None:
  RUN_GUNICORN = (os.environ.get('RUN_GUNICORN') == "True")
