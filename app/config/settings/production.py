from .base import *
DEBUG = False
# CORS_ORIGIN_WHITELIST = [
    
# ]
# CSRF_TRUSTED_ORIGINS = [
    
# ]
ALLOWED_HOSTS = ["https://stationery-rest-api.herokuapp.com",]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

import django_heroku
django_heroku.settings(locals())
# import cloudinary

# cloudinary.config(cloud_name='<cloud-name-here>',
#                   api_key='<api_key_here>',
#                   api_secret='<api_secret>')