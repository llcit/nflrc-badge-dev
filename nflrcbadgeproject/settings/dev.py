# dev.py
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/logout'

LOGIN_REDIRECT_URL = '/'