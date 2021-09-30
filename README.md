[![Build Status](https://api.travis-ci.com/frgmt/django-fernet-encrypted-fields.png)](https://travis-ci.com/frgmt/django-fernet-encrypted-fields)
[![Pypi Package](https://badge.fury.io/py/django-fernet-encrypted-fields.png)](http://badge.fury.io/py/django-fernet-encrypted-fields)


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

#### Available Fields

Currently build in and unit-tested fields. They have the same APIs as their non-encrypted counterparts.

- `EncryptedCharField`
- `EncryptedTextField`
- `EncryptedDateTimeField`
- `EncryptedIntegerField`
- `EncryptedFloatField`
- `EncryptedEmailField`
- `EncryptedBooleanField`

### Compatible Django Version

|Compatible Django Version|Specifically tested|
|---|---|
|`2.2`|:heavy_check_mark:|
|`3.0`|:heavy_check_mark:|
|`3.1`|:heavy_check_mark:|
|`3.2`|:heavy_check_mark:|
|`4.0`|:heavy_check_mark:|