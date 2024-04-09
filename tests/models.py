from encrypted_fields.fields import *


class TestModel(models.Model):
    char = EncryptedCharField(max_length=255, null=True, blank=True)
    text = EncryptedTextField(null=True, blank=True)
    datetime = EncryptedDateTimeField(null=True, blank=True)
    integer = EncryptedIntegerField(null=True, blank=True)
    date = EncryptedDateField(null=True, blank=True)
    floating = EncryptedFloatField(null=True, blank=True)
    email = EncryptedEmailField(null=True, blank=True)
    boolean = EncryptedBooleanField(default=False, null=True)
    json = EncryptedJSONField(default=dict, null=True, blank=True)
