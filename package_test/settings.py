DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

SECRET_KEY = 'abc'
SALT_KEY = 'xyz'

INSTALLED_APPS = (
    'encrypted_fields',
    'package_test'
)

MIDDLEWARE_CLASSES = []
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

