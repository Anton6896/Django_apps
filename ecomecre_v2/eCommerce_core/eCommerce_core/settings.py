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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b)*=%^6(^j8o^o5r8q)zp3-1jr+kp)@)d9#go(b80kvtaq@-=k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
    # main django root static files location <- emulation of some server
    os.path.dirname(BASE_DIR), 'static_cdn'
)
STATICFILES_DIRS = [
    # temp static location
    os.path.join(BASE_DIR, 'static_eCom'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_URL = 'users:login_page'
LOGIN_REDIRECT_URL = 'users:home_page'
LOGOUT_REDIRECT_URL = 'users:home_page'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

STRIPE_SECRET_KEY = "sk_test_51HfQZqEVa7KrzHgTJ7UvVaD5TLNHDHYWCZzVAn4YYdepEG" \
                    "Pli8BNKuMEE6wgKcXqsmfPrAeU73scz70DvbCGeBjs00kvs9An1q"
STRIPE_PUB_KEY = "pk_test_51HfQZqEVa7KrzHgTgqkamdkzgINVOPISYba6Jjo8yjF3KvQslC" \
                 "8RVpgm1qA79Yt9MA396lxSPpk5wmS3UakvpIna00BjEUpDLp"

STRIPE_LISTENER_CODE = "whsec_Fzg5Nt0vQ3BoCdq8zq8o8XylrATujJdb"
