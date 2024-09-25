"""
Django settings for interclasse project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [os.getenv('HOST')]


# Application definition

INSTALLED_APPS = [
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'interclasse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'interclasse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

if (os.getenv("DBTYPE") == "MySQL" or os.getenv("DBTYPE") == "mysql"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv("DBNAME"),
            'USER': os.getenv("DBUSER"),
            'PASSWORD': os.getenv("DBPASSWORD"),
            # Or an IP Address that your DB is hosted on
            'HOST': os.getenv("DBHOST"),
            'PORT': os.getenv("DBPORT"),
        }
    }

elif (os.getenv("DBTYPE") == "SQLite3" or os.getenv("DBTYPE") == "sqlite3"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR / 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'

if (os.getenv("ENVIRONMENT") == 'DEV' or os.getenv("ENVIRONMENT") == 'dev'):
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static/')
    ]
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

elif (os.getenv("ENVIRONMENT") == 'PROD' or os.getenv("ENVIRONMENT") == 'prod'):
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static/')
    ]
    MEDIA_ROOT = '/var/www/html/trancadura/media/'
    STATIC_ROOT = '/var/www/html/trancadura/static'

X_FRAME_OPTIONS = 'SAMEORIGIN'

CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['http://'+os.getenv('HOST'), 'https://'+os.getenv('HOST')]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
