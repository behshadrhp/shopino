import os
import dj_database_url
from .common import *

DEBUG = os.environ['DEBUG']

ALLOWED_HOSTS = ['https://behshadrhp.iran.liara.run']

SECRET_KEY = os.environ['SECRET_KEY']


DATABASES = {
    'default': dj_database_url.config()
}

CORS_ALLOWED_ORIGINS = os.environ['CORS_ALLOWED_ORIGINS']