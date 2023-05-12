import os

from environs import Env
import dj_database_url


env = Env()
env.read_env()


db_url = env('DB_URL')
DATABASES = {'default': dj_database_url.config(default=db_url)}


INSTALLED_APPS = ['datacenter']

SECRET_KEY = 'REPLACE_ME'

DEBUG = env.bool('DEBUG', True)

ROOT_URLCONF = 'project.urls'

ALLOWED_HOSTS = ['*']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
    },
]


USE_L10N = True

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
