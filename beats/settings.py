"""
Django settings for beats project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
from decouple import config
from pathlib import Path
import os

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qbvu(n2$xjb1o(9nbfe_!ay%x#z^)51vzmm_55pjd$+itrr-p)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ 'twinii-beats-393d87d854a4.herokuapp.com', '8000-rwinterburn-ciproject4-e3jnjjwfa8p.ws.codeinstitute-ide.net','8000-rwinterburn-ciproject4-5lr2qut07wl.ws.codeinstitute-ide.net','8000-rwinterburn-ciproject4-cnhtlmzoj3b.ws-eu117.gitpod.io','8000-rwinterburn-ciproject4-vqkeogj33da.ws-eu117.gitpod.io', '8000-rwinterburn-ciproject4-j341iks4fk8.ws-eu116.gitpod.io', '8000-rwinterburn-ciproject4-636qs5xvb6b.ws-eu116.gitpod.io']

LOGIN_REDIRECT_URL = '/profiles/'

CSRF_TRUSTED_ORIGINS = ['https://8000-rwinterburn-ciproject4-5lr2qut07wl.ws.codeinstitute-ide.net', 'https://8000-rwinterburn-ciproject4-e3jnjjwfa8p.ws.codeinstitute-ide.net','https://8000-rwinterburn-ciproject4-636qs5xvb6b.ws-eu117.gitpod.io', 'https://8000-rwinterburn-ciproject4-vqkeogj33da.ws-eu117.gitpod.io', 'https://8000-rwinterburn-ciproject4-cnhtlmzoj3b.ws-eu117.gitpod.io',]

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'instrumentals',
    'profiles',
    'bag',
    'checkout',
    'crispy_forms',
    
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    
]

ROOT_URLCONF = 'beats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /'templates'],
  # Ensure this points to the correct directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bag.context_processors.cart_items', 
                 # Your custom context processor
            ],
        },
    },
]



WSGI_APPLICATION = 'beats.wsgi.application'


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

STATIC_URL = "static/"

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Could be "none", "optional", or "mandatory"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  # Could be "username", "email", or "username_email"

SITE_ID = 1




STRIPE_CURRENCY = 'gbp'
# Stripe keys
STRIPE_PUBLIC_KEY = ('pk_test_51QMs27DNIGFfmTD08gW65dE0pAuBD5kuuZSiJgXoMpwkVHBVkso5IRVXHupM6IWNzqosRiSIEdO5p2PpH9RDh4p900aCJeCn5d')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET')
print('WH: ', STRIPE_WH_SECRET)

