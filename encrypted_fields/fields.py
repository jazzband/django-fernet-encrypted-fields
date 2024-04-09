import base64
import json

from cryptography.fernet import Fernet, MultiFernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property
from django.utils.encoding import force_bytes, force_str


class EncryptedFieldMixin:
    @cached_property
    def keys(self):
        keys = []
        salt_keys = (
            settings.SALT_KEY
            if isinstance(settings.SALT_KEY, list)
            else [settings.SALT_KEY]
        )
        for salt_key in salt_keys:
            salt = force_bytes(salt_key)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend(),
            )
            keys.append(
                base64.urlsafe_b64encode(kdf.derive(force_bytes(settings.SECRET_KEY)))
            )
        return keys

    @cached_property
    def f(self):
        if len(self.keys) == 1:
            return Fernet(self.keys[0])
        return MultiFernet([Fernet(k) for k in self.keys])

    def get_internal_type(self):
        """
        To treat everything as text
        """
        return getattr(self, "_internal_type", "TextField")

    def get_prep_value(self, value):
        value = super().get_prep_value(value)
        if value:
            if not isinstance(value, str):
                value = str(value)
            return force_str(self.f.encrypt(force_bytes(value)))
        return None

    def get_db_prep_value(self, value, connection, prepared=False):
        if not prepared:
            value = self.get_prep_value(value)
        return value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def decrypt(self, value):
        try:
            value = force_str(self.f.decrypt(force_bytes(value)))
        except (InvalidToken, UnicodeEncodeError):
            pass
        return value

    def to_python(self, value):
        if (
            value is None
            or not isinstance(value, str)
            or hasattr(self, "_already_decrypted")
        ):
            return value

        value = self.decrypt(value)
        return super().to_python(value)

    def clean(self, value, model_instance):
        """
        Create and assign a semaphore so that to_python method will not try to decrypt an already decrypted value
        during cleaning of a form
        """
        self._already_decrypted = True
        ret = super().clean(value, model_instance)
        del self._already_decrypted
        return ret

    @cached_property
    def validators(self):
        # Temporarily pretend to be whatever type of field we're masquerading
        # as, for purposes of constructing validators (needed for
        # IntegerField and subclasses).
        self._internal_type = super().get_internal_type()
        try:
            return super().validators
        finally:
            del self._internal_type


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


class EncryptedJSONField(EncryptedFieldMixin, models.JSONField):
    def _encrypt_values(self, value):
        if isinstance(value, dict):
            return {key: self._encrypt_values(data) for key, data in value.items()}
        elif isinstance(value, list):
            return [self._encrypt_values(data) for data in value]
        else:
            value = str(value)
        return force_str(self.f.encrypt(force_bytes(value)))

    def _decrypt_values(self, value):
        if value is None:
            return value
        if isinstance(value, dict):
            return {key: self._decrypt_values(data) for key, data in value.items()}
        elif isinstance(value, list):
            return [self._decrypt_values(data) for data in value]
        else:
            value = str(value)
        return force_str(self.f.decrypt(force_bytes(value)))

    def get_prep_value(self, value):
        return json.dumps(self._encrypt_values(value=value), cls=self.encoder)

    def get_internal_type(self):
        return "JSONField"

    def decrypt(self, value):
        try:
            value = self._decrypt_values(value=json.loads(value))
        except (InvalidToken, UnicodeEncodeError):
            pass
        return value
