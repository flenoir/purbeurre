from . import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'purbeurre_db',
        'USER': 'postgres',
        'PASSWORD': 'l1ghtm4n',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}