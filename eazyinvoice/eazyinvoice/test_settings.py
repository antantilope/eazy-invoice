

from eazyinvoice.settings import *


IS_PROD = False

# Faster insecure hashing for testing only
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'testdb.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []
