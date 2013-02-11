import urlparse
import os
import json


DEBUG = True



def paasIs(name='not set'): # Returns whether is running in a PaaS if invoked without a name
    PaaS = ('OPENSHIFT_APP_NAME', 'VCAP_SERVICES')
    for env in PaaS:
        if env in os.environ:
            if name == 'not set' or name in env:
                return True
    return False

backend = {'engine':'django.db.backends.sqlite3', 'name':'../../data/production.db', 'user':'', 'password':'', 'hostname':'', 'port':''} #default

if paasIs('OPENSHIFT'): # OPENSHIFT
    for db in ('OPENSHIFT_MYSQL_DB_URL', 'OPENSHIFT_POSTGRESQL_DB_URL'):
        if db in os.environ:
            backend['name'] = os.environ['OPENSHIFT_APP_NAME']
            if 'MYSQL' in db:
                url = urlparse.urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
                backend['engine'] = 'django.db.backends.mysql'
            else:
                url = urlparse.urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))
                backend['engine'] = 'django.db.backends.postgresql_psycopg2'
            backend['user'] = url.username
            backend['password'] = url.password
            backend['hostname'] = url.hostname
            backend['port'] = url.port

    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')

elif paasIs('VCAP'): # CloudFoundry Core
    services = json.loads(os.environ['VCAP_SERVICES'])
    if 'postgresql' in services:
        backend = services['postgresql-9.1'][0]['credentials']
        backend['engine'] = 'django.db.backends.postgresql_psycopg2'
    elif 'mysql-5.1' in services:
        backend = services['mysql-5.1'][0]['credentials']
        backend['engine'] = 'django.db.backends.mysql'

DATABASES = {
    'default': {
        'ENGINE': backend['engine'],
        'NAME': backend['name'],
        'USER': backend['user'],
        'PASSWORD': backend['password'],
        'HOST': backend['hostname'],
        'PORT': backend['port'],
    }
}


# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'

ADMINS = (
# ('Your Name', 'your_email@domain.com'),
)
SECRET_KEY = "e4c025c5-19c5-eli5-bf8d-90ac32de137085bdf025-d693-4e69-bde1-d277a3d57e2dbd2b41d2-7cb3-4f9d-b2f9-407421e996ae"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

#CACHE_MIDDLEWARE_SECONDS = 60
#
#CACHE_MIDDLEWARE_KEY_PREFIX = "%(proj_name)s"
#
#CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.memcached.MemcachedCache",
#        "LOCATION": "127.0.0.1:11211",
#    }
#}
#
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"



# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse'
#         }
#     },
#     'handlers': {
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler'
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     }
# }
