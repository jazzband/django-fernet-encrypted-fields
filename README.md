[![Build Status](https://github.com/jazzband/django-fernet-encrypted-fields/actions/workflows/lint-and-test.yml/badge.svg)](https://github.com/jazzband/django-fernet-encrypted-fields/actions/workflows/lint-and-test.yml)
[![Pypi Package](https://badge.fury.io/py/django-fernet-encrypted-fields.png)](http://badge.fury.io/py/django-fernet-encrypted-fields)
[![Jazzband](https://jazzband.co/static/img/badge.svg)](https://jazzband.co/)


### Django Fernet Encrypted Fields

This package was created as a successor to [django-encrypted-fields](https://github.com/defrex/django-encrypted-fields).

#### Getting Started
```shell
$ pip install django-fernet-encrypted-fields
```
In your `settings.py`, set random SALT_KEY
```python
SALT_KEY = '0123456789abcdefghijklmnopqrstuvwxyz'
```

Then, in `models.py`
```python
from encrypted_fields.fields import EncryptedTextField

class MyModel(models.Model):
    text_field = EncryptedTextField()
```
Use your model as normal and your data will be encrypted in the database.

#### Rotating SALT keys
You can rotate salt keys by turning the ```SALT_KEY``` settings.py entry into a list.  The first key will be used to encrypt all new data, and decryption of existing values will be attempted with all given keys in order. This is useful for key rotation: place a new key at the head of the list for use with all new or changed data, but existing values encrypted with old keys will still be accessible

```python
SALT_KEY = [
    'zyxwvutsrqponmlkjihgfedcba9876543210',
    '0123456789abcdefghijklmnopqrstuvwxyz'
]
```

If you wish to update the existing encrypted records simply load and re-save the models to use the new key.

```
for obj in MuModel.objects.all():
    obj.save()
```


#### Available Fields

Currently build in and unit-tested fields. They have the same APIs as their non-encrypted counterparts.

- `EncryptedCharField`
- `EncryptedTextField`
- `EncryptedDateTimeField`
- `EncryptedIntegerField`
- `EncryptedFloatField`
- `EncryptedEmailField`
- `EncryptedBooleanField`
- `EncryptedJSONField`

### Compatible Django Version

| Compatible Django Version |Specifically tested|
|---------------------------|---|
| `3.2`                     |:heavy_check_mark:|
| `4.0`                     |:heavy_check_mark:|
| `4.1`                     |:heavy_check_mark:|
| `4.2`                     |:heavy_check_mark:|
| `5.0`                     |:heavy_check_mark:|
