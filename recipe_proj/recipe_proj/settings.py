"""
Django settings for recipe_proj project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv() #S3_ACCESS_KEY, S3_SECRET_KEY
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f0l@sab@werq(wb#!$m_qda+8dt(_txdlz3*o#s3822!fpp7px'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'recipe_list.apps.RecipeListConfig',
    'recipe_accounts.apps.RecipeAccountsConfig',
    'api.apps.ApiConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce'
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

ROOT_URLCONF = 'recipe_proj.urls'

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

WSGI_APPLICATION = 'recipe_proj.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get('DB_HOST'),
        "NAME": os.environ.get('DB_NAME'),
        "USER": os.environ.get('DB_USER'),
        "PASSWORD": os.environ.get('DB_PASS')
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

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Перенаправление при успешном входе в аккаунт
LOGIN_REDIRECT_URL = 'home'

#Перенаправление при успешном выходе их аккаунта
LOGOUT_REDIRECT_URL = 'home'

# Хранение изображений рецептов
MEDIA_ROOT = os.path.join(BASE_DIR, 'recipes_image')

#URL рецептов
MEDIA_URL = '/image/'

#Настройка панели ввода
'''TINYMCE_PROFILE = {
    'theme': 'modern',
    'plugins': 'noneditable advlist autolink link lists charmap hr searchreplace wordcount visualblocks visualchars code insertdatetime save table contextmenu directionality paste textcolor',
    'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | forecolor backcolor | upload_button',
    'noneditable_leave_contenteditable': 'true',
    'setup': 'addCustomButtons',
    'content_css': os.path.join(STATIC_URL, "mycss/tinymce.css"),
    'relative_urls': False,
    'remove_script_host': True,
    'document_base_url': APP_HOST_URL,
    'removed_menuitems': 'newdocument'
}'''

#Категории:
CATEGORY_LIST = (
        ('Первое блюдо', 'Первое блюдо'),
        ('Второе блюдо', 'Второе блюдо'),
        ('Напитки', 'Напитки'),
        ('Завтрак', 'Завтрак'),
    )

#Настройка отправки на почту
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#Настройка отображения
START_COUNT_VIEW = 9

#Настройки ручного кеша
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "db": '0'
        }
    }
}
COMMENTS_LIST_NAME = 'comment_list'
COMMENTS_LIST_TTL = 60 * 60

RECIPE_LIST_NAME = "recipe_list"
RECIPE_LIST_TTL = 60 * 60

USER_OBJS_NAME = 'users'
USER_OBJS_TTL = 60 * 60

#celery

CELERY_BROKER_URL = 'redis://redis:6379/1'

#s3 (запихнуть все в переменные вируального кружения)

S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY')
S3_ENDPOINT_URL = 'https://s3.storage.selcloud.ru'
S3_BUCKET_NAME = 'recipe-public-bucket'
S3_REGION_NAME = 'ru-1'