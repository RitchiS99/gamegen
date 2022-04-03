"""
Django settings for spielegenerator project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import ldap
import environ
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-bt)#774$5zhk7w*d@ycfrtos0*5e90vln1i-k!qa87-d7yj^p_'
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')

REGISTRATION_MAIL_TEXT = env('REGISTRATION_MAIL_TEXT')

NAME = env('NAME')

LANGUAGE_CODE = env('LANGUAGE_CODE')

ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]

CSRF_TRUSTED_ORIGINS = [env('TRUSTED_ORIGINS')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'scripts',
    'login',
    'editor',
    'locale',
    'importer',
]

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'spielegenerator.urls'

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

WSGI_APPLICATION = 'spielegenerator.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


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

# LANGUAGE_CODE = 'en-us'


TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND=env('EMAIL_BACKEND')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


if env('USE_LDAP')=='True':
    LDAP_CHANGE_PASSWORD = env('LDAP_CHANGE_PASSWORD')
    AUTHENTICATION_BACKENDS.append("django_auth_ldap.backend.LDAPBackend")
    AUTH_LDAP_SERVER_URI = env('AUTH_LDAP_SERVER_URI')
    AUTH_LDAP_BIND_DN = env('AUTH_LDAP_BIND_DN')
    AUTH_LDAP_BIND_PASSWORD = env('AUTH_LDAP_BIND_PASSWORD')
    AUTH_LDAP_USER_SEARCH = LDAPSearch(
        env('AUTH_LDAP_USER_SEARCH_DN'), ldap.SCOPE_SUBTREE, "(uid=%(user)s)"
    )
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
        env('AUTH_LDAP_GROUP_SEARCH_DN'),
        ldap.SCOPE_SUBTREE,
        "(objectClass=groupOfNames)",
    )
    # AUTH_LDAP_GROUP_TYPE = env('AUTH_LDAP_GROUP_TYPE')
    AUTH_LDAP_REQUIRE_GROUP = env('AUTH_LDAP_REQUIRE_GROUP')
    AUTH_LDAP_ALWAYS_UPDATE_USER = env('AUTH_LDAP_ALWAYS_UPDATE_USER')


    # Bleibt drinnen
    AUTH_LDAP_USER_ATTR_MAP = {
        "first_name": "givenName",
        "last_name": "sn",
        "email": "mail",
        "password": "password"
    }
    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_staff": env('LDAP_IS_STAFF'),
        "is_superuser": env('LDAP_IS_SUPERUSER'),
    }
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()