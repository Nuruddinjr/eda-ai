"""
Django settings for admin project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#jll5#itwnimxepxq6=o!@d+vub^1dbh(7(xpqo6t5zf4&$p-a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'payme'
]
AUTH_USER_MODEL = 'home.Users'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'admin.urls'

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

WSGI_APPLICATION = 'admin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'






PAYMENT_VARIANTS = {
    'click': ('click_api.ClickProvider', {
        'merchant_id': 13720,
        'merchant_service_id': 37207,
        'merchant_user_id': 46016,
        'secret_key': '2YH7UUb8w2eDKrL'
    })
}


CSRF_COOKIE_SECURE = False
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost",
]





PAYME_ID = "611b587a754e932e68fe396d"
PAYME_ACCOUNT = "order_id"
PAYME_CALL_BACK_URL = "https://ec3c-5-133-120-251.ngrok-free.app/payme/callback"
PAYME_URL = "https://checkout.paycom.uz"
ORDER_MODEL = "home.models.OrderTransactionsModel"

PAYME: dict = {
    'PAYME_ID': '611b587a754e932e68fe396d',
    'PAYME_KEY': 'Y8qi0TMazXAG?RCpAj7PNDInZYr2RTEjtxCe',
    'PAYME_URL': 'https://checkout.test.paycom.uz/api/',
    'PAYME_CALL_BACK_URL': 'https://ec3c-5-133-120-251.ngrok-free.app/payme/callback',  # merchant api callback url
    'PAYME_ACCOUNT': 'order_id',
}
PAYMENT_HOST = 'https://mysafar.uz'
PAYMENT_USES_SSL = True  # set the True value if you are using the SSL
PAYMENT_MODEL = 'home.Payment'