from .base import *
from decouple import config
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', "asdf61(&jz-la=8-u5yf-ay-nid73)#(_a(wqpo#d++jlw%1ou&v")
# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*', 'https://whitsundays.herokuapp.com/'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
