from config.django.base import *
from config.env import ROOT_DIR


DEBUG = True
SECRET_KEY = 'dev-only-insecure-key'
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ROOT_DIR / 'my-local-sqlite.sqlite3',
    }
}
