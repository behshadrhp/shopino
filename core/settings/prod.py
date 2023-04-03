import os
import dj_database_url
from .common import *

DEBUG = False

ALLOWED_HOSTS = ['https://behshadrhp.iran.liara.run']

SECRET_KEY = os.environ['secret_key']


DATABASES = {
    'default': dj_database_url.config()
}