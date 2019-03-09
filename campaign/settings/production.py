from .base import *
from decouple import config

SECRET_KEY = config('SECRET_KEY')


DEBUG = False

ALLOWED_HOSTS = ['*', 'https://whitsundays.herokuapp.com/']

#BASE_URL = 'https://felix-hall.com'

try:
    from .local import *
except ImportError:
    pass
