from datetime import timedelta
from os import environ, path
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://27c387d7ccbd4abcbfac93a68f2075e8@o516792.ingest.sentry.io/5623721",    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,

    # By default the SDK will try to use the SENTRY_RELEASE
    # environment variable, or infer a git commit
    # SHA as release, however you may want to set
    # something more human-readable.
    # release="myapp@1.0.0",
)


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^21#&4i58g@o&k-n$brbb371x8)qf@l(#c9jefv7_&-2zi+p)e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['84.238.224.124', 'api.hacktues.com', 'admin.hacktues.com',
                 'hacktues.pythonanywhere.com', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'wave1.apps.Wave1Config',
    'wave2.apps.Wave2Config',
    'rest_framework',
    'corsheaders',
    'django_email_verification',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES':
        ['rest_framework.permissions.AllowAny'],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://hacktues.com', 'http://localhost:3000',
                        'https://beta.hacktues.com']

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
}

def EMAIL_VERIFIED_CALLBACK(user):
    user.is_active = True

SENDGRID_SANDBOX_MODE_IN_DEBUG = False
EMAIL_FROM_ADDRESS = 'no-reply@hacktues.com'
EMAIL_MAIL_SUBJECT = 'hacktues mail confirmation'
EMAIL_MAIL_HTML = 'mail_body.html'
EMAIL_MAIL_PLAIN = 'mail_body.txt'
EMAIL_TOKEN_LIFE = 60 * 60
EMAIL_PAGE_TEMPLATE = 'confirm_template.html'
EMAIL_PAGE_DOMAIN = 'https://api.hacktues.com/'

SENDGRID_API_KEY = environ.get('apikey')
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# EMAIL_SERVER = EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_ADDRESS = EMAIL_HOST_USER = 'yoan.p.dzhelekarski.2017@elsys-bg.org'
# EMAIL_PASSWORD = EMAIL_HOST_PASSWORD = 'dhrabhrkoklvboax'
# EMAIL_USE_TLS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hacktues$default',
        'USER': 'hacktues',
        'PASSWORD': 'P8)yx?FpA2+hh!Hv',
        'HOST': 'localhost',
        'TIME_ZONE': 'Europe/Sofia',
        'TEST': {
            'NAME': 'hacktues$test_default',
        },
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            "charset": "utf8mb4",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'wave2.User'
# SILENCED_SYSTEM_CHECKS = ["fields.E304"]

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'bg-BG'

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = path.join(BASE_DIR, "static")
