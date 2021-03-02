"""
Django settings for eCommerce_core project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# after rename and move the settings file need to add one more parent section ! <<--
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b)*=%^6(^j8o^o5r8q)zp3-1jr+kp)@)d9#go(b80kvtaq@-=k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'users',
    'crispy_forms',  # https://django-crispy-forms.readthedocs.io/en/latest/install.html
    'products',
    'search',
    'tags',
    'carts',
    'fontawesome-free',  # https://fontawesome.com/
    'order',
    'billing',
    'accounts',
    'analytics',
    'django.contrib.sites',
    'marketing',


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

ROOT_URLCONF = 'eCommerce_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'users/templates'),
            os.path.join(BASE_DIR, 'products/templates'),
            os.path.join(BASE_DIR, 'search/templates'),  # <- costume search
            os.path.join(BASE_DIR, 'carts/templates'),
            os.path.join(BASE_DIR, 'order/templates'),
            os.path.join(BASE_DIR, 'billing/templates'),

        ],
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

WSGI_APPLICATION = 'eCommerce_core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# AUTH_USER_MODEL = 'accounts.User'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(
    os.path.dirname(BASE_DIR), 'static_cdn'
)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_eCom'),  # temp static location
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'users:login_page'
LOGIN_REDIRECT_URL = 'users:home_page'
LOGOUT_REDIRECT_URL = 'users:home_page'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

#  all this keys is for learning purposes only not for production
#  have no real data at this keys available !
#  all key must be stored ad variables on production  !

STRIPE_SECRET_KEY = "sk_test_51HfQZqEVa7KrzHgTJ7UvVaD5TLNHDHYWCZzVAn4YYdepEG" \
                    "Pli8BNKuMEE6wgKcXqsmfPrAeU73scz70DvbCGeBjs00kvs9An1q"
STRIPE_PUB_KEY = "pk_test_51HfQZqEVa7KrzHgTgqkamdkzgINVOPISYba6Jjo8yjF3KvQslC" \
                 "8RVpgm1qA79Yt9MA396lxSPpk5wmS3UakvpIna00BjEUpDLp"
STRIPE_LISTENER_CODE = "whsec_Fzg5Nt0vQ3BoCdq8zq8o8XylrATujJdb"

MAILCHIMP_API_KEY = '2de1455f2e28741daec3340709f0b4c2-us1'
MAILCHIMP_DATA_CENTER = 'us1'
MAILCHIMP_LIST_ID = '511f14dc2a'

# https encryption (let's encrypt )  -> on
CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True
