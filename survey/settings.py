
from pathlib import Path
import os
from django.contrib.messages import constants as messages
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1
SITE_URL = 'localhost:8000'


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    #My Apps
    'core',
    'surveyscaled',
    'experiment',
    'users',
    'user_registration_landing_page',
    'ecommerce_store',
    'price_promotion_landing_page',
    'charity_donation_app',
    'event_registration_page',
    'download_page',
    'video_view_page',
    
    # 3rd Party Apps
    'storages',          # used for AWS s3 bucket storage
    'widget_tweaks',     # uses 'django-widget-tweaks' app
    'login_required',    # uses 'django-login-required-middleware' app
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'login_required.middleware.LoginRequiredMiddleware',    # middleware used for global login
]

ROOT_URLCONF = 'survey.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'experiment.context_processor.get_common_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'survey.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


if DEBUG:
    # Databse configration for development using SQLite
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME':  'db.sqlite3',
    #     }
    # }
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', #Database Engine
            'NAME': env('POSTGRES_DB'), #Database Name
            'USER': env("POSTGRES_USER"), #User Name
            'PASSWORD': env("POSTGRES_PASSWORD"), #Password
            'HOST': env("POSTGRES_HOST"), #Host Name (localhost)
            'PORT': env("POSTGRES_PORT"), #Access Port (Leave Blank)
        },
        'testdatabase': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', #Database Engine
            'NAME': env('POSTGRES_DB_FLASK'), #Database Name
            'USER': env("POSTGRES_USER_FLASK"), #User Name
            'PASSWORD': env("POSTGRES_PASSWORD_FLASK"), #Password
            'HOST': env("POSTGRES_HOST_FLASK"), #Host Name (localhost)
            'PORT': env("POSTGRES_PORT_FLASK"), #Access Port (Leave Blank)
        },
    }

else:
    # Database configuration for deployment using MySql
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', #Database Engine
            'NAME': env('POSTGRES_DB'), #Database Name
            'USER': env("POSTGRES_USER"), #User Name
            'PASSWORD': env("POSTGRES_PASSWORD"), #Password
            'HOST': env("POSTGRES_HOST"), #Host Name (localhost)
            'PORT': env("POSTGRES_PORT"), #Host Name (Leave Blank)
        }
    }

DATABASE_ROUTERS = ['survey.router.DatabaseRouter']


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_files')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media_files")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Tags to load BootStrap class for Django message framework
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

#Registration with Confirmation Mail for development setup for gmail
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = 'Survey Management Team <admin@localhost:8000.com>' 
    APPLICATION_EMAIL = 'admin@admin.com'

#Registration with Confirmation Mail for deployment
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_USE_TLS = False
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAULT_FROM_EMAIL = ''


if DEBUG:
    pass

else:
    #S3 BUCKETS CONFIG
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = None
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    S3_URL = '//%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = '//%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_ROOT = MEDIA_URL
    # STATIC_URL = S3_URL + 'static/'
    # ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


'''
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
'''

# MAILCHIMP CREDENTIALS
MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')
MAILCHIMP_DATA_CENTER = env('MAILCHIMP_DATA_CENTER')
MAILCHIMP_EMAIL_LIST_ID = env('MAILCHIMP_EMAIL_LIST_ID')

LOGIN_URL = 'users:login'                  # sets the 'login' page as default when user tries to illegally access profile or other hidden pages
LOGIN_REDIRECT_URL = 'core:home'           # sets the login redirect to the 'home' page after login
LOGOUT_REDIRECT_URL = 'users:login'        # sets the logout redirect to the 'login' page after logout

LOGIN_REQUIRED_IGNORE_VIEW_NAMES = [       # urls ignored by the login_required. Can be accessed with out logging in
    'users:login',
    'users:registration',
    'users:logout',
    'surveyscaled:upload-survey'
    'surveyscaled:thank-you-page',
]