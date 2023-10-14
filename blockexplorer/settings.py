"""
Django settings for blockexplorer project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import re
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))
LOCALE_PATHS = (PROJECT_PATH + "/locale/",)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG') == 'True':
    DEBUG = True
else:
    DEBUG = False
if os.getenv('TEMPLATE_DEBUG') == 'True':
    TDEBUG = True
else:
    TDEBUG = False

# DDT can cause extreme slowness clocking template rendering CPU times
if os.getenv('DISABLE_DEBUG_TOOLBAR') == 'False':
    DISABLE_DEBUG_TOOLBAR = False
else:
    DISABLE_DEBUG_TOOLBAR = True

ALLOWED_HOSTS = [
        'live.blockcypher.com',
        'blockcypher.herokuapp.com',
        'blockcypher-dev.herokuapp.com',
        'blockcypher-heroku-22.herokuapp.com',
        '127.0.0.1',
        'localhost'
        ]

ADMINS = (
    ('Michael Flaxman', 'mflaxman@gmail.com'),
)

IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'raven.contrib.django.raven_compat',
    'crispy_forms',
    'storages',
    'addresses',
    'transactions',
    'users',
    'emails',
    'services',
)

MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'blockexplorer.urls'

WSGI_APPLICATION = 'blockexplorer.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Parse database configuration from $DATABASE_URL
# http://stackoverflow.com/a/11100175
DJ_DEFAULT_URL = os.getenv('DJ_DEFAULT_URL', 'postgres://localhost')
DATABASES = {'default': dj_database_url.config(default=DJ_DEFAULT_URL)}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'users.AuthUser'
LOGIN_URL = '/login'

# Languages
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('en-us', 'English'),
)
if os.getenv('ENABLE_TRANSLATIONS') == 'False':
    ENABLE_TRANSLATIONS = False
else:
    ENABLE_TRANSLATIONS = True
    MIDDLEWARE += ('django.middleware.locale.LocaleMiddleware',)
    LANGUAGES += (('es', 'Spanish'),)

# Yay crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'
CRISPY_ALLOWED_TEMPLATE_PACKS = ('bootstrap', 'bootstrap3')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

TEMPLATES = [
    {
        'BACKEND':'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': (os.path.join(PROJECT_PATH, 'templates'),),
        'OPTIONS': {
            'context_processors': [
                'blockexplorer.context_processors.get_user_units',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
            ],
            'debug': TDEBUG,
        },
    }
]

PRODUCTION_DOMAIN = 'live.blockcypher.com'
STAGING_DOMAIN = 'TODO'
SITE_DOMAIN = os.getenv('SITE_DOMAIN', PRODUCTION_DOMAIN)

# SSL and BASE_URL settings for Production, Staging and Local:
if SITE_DOMAIN in (PRODUCTION_DOMAIN, STAGING_DOMAIN):
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    BASE_URL = 'https://%s' % SITE_DOMAIN
    # FIXME:
    CSRF_COOKIE_SECURE = True
    MIDDLEWARE += ('django.middleware.security.SecurityMiddleware',)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
else:
    BASE_URL = 'http://%s' % SITE_DOMAIN
    if not DISABLE_DEBUG_TOOLBAR:
        # FIXME: this should work on staging too, but I can't get it to work with gunicorn
        DEBUG_TOOLBAR_PATCH_SETTINGS = True


IS_PRODUCTION = (SITE_DOMAIN == PRODUCTION_DOMAIN)

if IS_PRODUCTION:
    EMAIL_DEV_PREFIX = False
else:
    EMAIL_DEV_PREFIX = True
    if not DISABLE_DEBUG_TOOLBAR:
        # Enable debug toolbar on local and staging
        MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE
        INSTALLED_APPS += ('debug_toolbar', )

if not DISABLE_DEBUG_TOOLBAR:
    # Debug Toolbar
    INTERNAL_IPS = (
            '127.0.0.1',
            'localhost',
            )

BLOCKCYPHER_API_KEY = os.getenv('BLOCKCYPHER_API_KEY')
BLOCKCYPHER_PUBLIC_KEY = '31c49f33f35c85a8f4d9845a754f7c8e'

POSTMARK_SMTP_SERVER = 'smtp.postmarkapp.com'
POSTMARK_SENDER = 'Blockcypher Notifications <notifications@blockcypher.com>'
POSTMARK_TEST_MODE = os.getenv('POSTMARK_TEST_MODE', False)
POSTMARK_API_KEY = os.getenv('POSTMARK_API_KEY')
if not POSTMARK_API_KEY:
    print('WARNING: without a POSTMARK_API_KEY you cannot send emails')

EMAIL_BACKEND = 'postmark.django_backend.EmailBackend'

SENTRY_DSN = os.getenv('SENTRY_DSN')

# Wallet Name
WNS_URL_BASE = 'https://pubapi.netki.com/api/wallet_lookup'

DEFAULT_USER_UNIT = 'btc'

# http://scanova.io/blog/engineering/2014/05/21/error-logging-in-javascript-and-python-using-sentry/
LOGGING = {
    'version': 1,
    # https://docs.djangoproject.com/en/dev/topics/logging/#configuring-logging
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry', 'console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

if DEBUG:
    print('-'*75)
    print('SITE_DOMAIN is set to %s' % SITE_DOMAIN)
    print('-'*75)
