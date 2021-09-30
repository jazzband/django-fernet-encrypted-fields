import base64
from django.conf import settings
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.db import models


class EncryptedFieldMixin(object):
    salt = bytes(settings.SALT_KEY, 'utf-8')
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())

    key = base64.urlsafe_b64encode(kdf.derive(settings.SECRET_KEY.encode('utf-8')))
    f = Fernet(key)

    def get_internal_type(self):
        """
        To treat everything as text
        """
        return 'TextField'

    def get_prep_value(self, value):
        if value:
            if not isinstance(value, str):
                value = str(value)
            return self.f.encrypt(bytes(value, 'utf-8')).decode('utf-8')
        return None

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if value is None or not isinstance(value, str):
            return value
        value = self.f.decrypt(bytes(value, 'utf-8')).decode('utf-8')
        return super(EncryptedFieldMixin, self).to_python(value)


class EncryptedCharField(EncryptedFieldMixin, models.CharField):
    pass


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    pass


class EncryptedDateTimeField(EncryptedFieldMixin, models.DateTimeField):
    pass


class EncryptedIntegerField(EncryptedFieldMixin, models.IntegerField):
    pass


class EncryptedDateField(EncryptedFieldMixin, models.DateField):
    pass


class EncryptedFloatField(EncryptedFieldMixin, models.FloatField):
    pass


class EncryptedEmailField(EncryptedFieldMixin, models.EmailField):
    pass


class EncryptedBooleanField(EncryptedFieldMixin, models.BooleanField):
    pass
