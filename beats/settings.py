
from decouple import config
from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = [ 'twinii-beats-393d87d854a4.herokuapp.com', '8000-rwinterburn-ciproject4-e3jnjjwfa8p.ws.codeinstitute-ide.net','8000-rwinterburn-ciproject4-5lr2qut07wl.ws.codeinstitute-ide.net','8000-rwinterburn-ciproject4-cnhtlmzoj3b.ws-eu117.gitpod.io','8000-rwinterburn-ciproject4-vqkeogj33da.ws-eu117.gitpod.io', '8000-rwinterburn-ciproject4-j341iks4fk8.ws-eu116.gitpod.io', '8000-rwinterburn-ciproject4-636qs5xvb6b.ws-eu116.gitpod.io']

LOGIN_REDIRECT_URL = '/profiles/'

CSRF_TRUSTED_ORIGINS = ['https://8000-rwinterburn-ciproject4-5lr2qut07wl.ws.codeinstitute-ide.net', 'https://8000-rwinterburn-ciproject4-e3jnjjwfa8p.ws.codeinstitute-ide.net','https://8000-rwinterburn-ciproject4-636qs5xvb6b.ws-eu117.gitpod.io', 'https://8000-rwinterburn-ciproject4-vqkeogj33da.ws-eu117.gitpod.io', 'https://8000-rwinterburn-ciproject4-cnhtlmzoj3b.ws-eu117.gitpod.io',]



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
    'storages',
    
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
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'bag.context_processors.cart_items', 
                 
            ],
        },
    },
]


ACCOUNT_EMAIL_VERIFICATION = 'none'
WSGI_APPLICATION = 'beats.wsgi.application'

if 'DATABASE_URL' in os.environ:

 DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))  
}
else:
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
    

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'


STATICFILES_DIRS = [
    BASE_DIR / "static",
]

if 'USE_AWS' in os.environ:
    AWS_STORAGE_BUCKET_NAME = 'twinii-beats'
    AWS_S3_REGION_NAME = 'eu-north-1'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'


    STATICFILES_STORAGE = 'custom_storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'

    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIAFILES_LOCATION}/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"  
ACCOUNT_AUTHENTICATION_METHOD = "username_email"  

SITE_ID = 1


STRIPE_CURRENCY = 'gbp'

STRIPE_PUBLIC_KEY = ("pk_test_51QMs27DNIGFfmTD08gW65dE0pAuBD5kuuZSiJgXoMpwkVHBVkso5IRVXHupM6IWNzqosRiSIEdO5p2PpH9RDh4p900aCJeCn5d")

STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET')



