from .common import *


DEBUG = True

SECRET_KEY = 'xmpq)%y#ne-v15)o2@=!66=mf*j*n^(qtb*^v+*8z!j3a*4pzf'

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'HOST': 'containers-us-west-105.railway.app',
        'PORT': '7773',
        'USER': 'postgres',
        'PASSWORD': 'AIP8zdncGFG3QlktaoEL'
    }
}
