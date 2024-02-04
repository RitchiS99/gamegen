"""
Django settings for gamegen project.

For more information on this file, see
https://docs.djangoproject.com/

"""

from pathlib import Path
import os
import environ

env = environ.Env()
environ.Env.read_env()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG')




NAME = env('NAME')

ALLOWED_HOSTS = [env('ALLOWED_HOSTS')]

CSRF_TRUSTED_ORIGINS = [env('TRUSTED_ORIGINS')]

CORS_ORIGIN_ALLOW_ALL = True

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework',
    'django_htmx',
    'requests',
    'modelclasses',
    'templates',
    'webpack_loader',
    'multiselectfield',
    'static',
    'home',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
]

ROOT_URLCONF = 'gamegen.urls'

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
            ],
        },
    },
]


if DEBUG=="True":
    WEBPACK_LOADER = {
            'DEFAULT': {
                'CACHE': False,
                'BUNDLE_DIR_NAME': 'dev/',
                'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.dev.json'),
                'POLL_INTERVAL': 0.1,
                'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
            }
        }
else:

    WEBPACK_LOADER = {
        'DEFAULT': {
            'CACHE': True,
            'BUNDLE_DIR_NAME': 'dist/',
            'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
            'POLL_INTERVAL': 0.1,
            'IGNORE': [r'.+\.hot-update.js', r'.+\.map'],
        }
    }



WSGI_APPLICATION = 'gamegen.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

gettext = lambda s: s
LANGUAGES = (
    ('de', gettext('Deutsch')),
    ('en', gettext('English')),
)

LANGUAGE_CODE = env('LANGUAGE_CODE')

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

MEDIA_ROOT = os.path.join(BASE_DIR, 'uploaded_files')
MEDIA_URL = '/media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'assets'),
]

LOGIN_URL = "/login"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}