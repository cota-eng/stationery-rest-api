from .base import *
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import environ
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))

# for cors
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True  # Access-control-Allow-Credentials: true

DEBUG = False

INSTALLED_APPS += (
    'storages',
    'django_cleanup.apps.CleanupConfig',
    # 'whitenoise.runserver_nostatic',
)

MIDDLEWARE += (
    'django.middleware.security.SecurityMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware',
)

"""
Django Security
"""
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE=True
# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_PRELOAD=True
# CORS_ORIGIN_WHITELIST = [
    
# ]
# CSRF_TRUSTED_ORIGINS = [
    
# ]
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ALLOWED_HOSTS = [".herokuapp.com",]

"""
DB
"""
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
DATABASES['default'].update(db_from_env)

"""
django heroku 
"""
import django_heroku
django_heroku.settings(locals())


"""
cloudinary
"""
# import cloudinary
# cloudinary.config(cloud_name='<cloud-name-here>',
#                   api_key='<api_key_here>',
#                   api_secret='<api_secret>')


"""
AWS-Settings
"""
AWS_ACCESS_KEY_ID = env('AWS_ACCESS')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'static' # s3バケット上のベースとなるファイルパス
AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

"""
static
"""
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
AWS_S3_SECURE_URLS = True

"""
Django-Storage
"""
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'