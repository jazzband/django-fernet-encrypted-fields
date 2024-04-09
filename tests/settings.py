DATABASES = {
    "default": {
        "ENGINE": "tests.sqlite3",
        "NAME": ":memory:",
    },
}

SECRET_KEY = "abc"
SALT_KEY = "xyz"

INSTALLED_APPS = ("encrypted_fields", "tests")

MIDDLEWARE_CLASSES = []
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
