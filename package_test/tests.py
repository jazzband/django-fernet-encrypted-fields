import json
import re

import pytest
from django.core.exceptions import ValidationError
from django.db import connection
from django.test import TestCase, override_settings
from django.utils import timezone

from .models import TestModel


class FieldTest(TestCase):
    def get_db_value(self, field: str, model_id: int) -> None:
        cursor = connection.cursor()
        cursor.execute(
            f"select {field} from package_test_testmodel where id = {model_id};"
        )
        return cursor.fetchone()[0]

    def test_char_field_encrypted(self) -> None:
        plaintext = "Oh hi, test reader!"

        model = TestModel()
        model.char = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("char", model.id)

        assert plaintext != ciphertext
        assert "test" not in ciphertext

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.char == plaintext

    def test_text_field_encrypted(self) -> None:
        plaintext = "Oh hi, test reader!" * 10

        model = TestModel()
        model.text = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("text", model.id)

        assert plaintext != ciphertext
        assert "test" not in ciphertext

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.text == plaintext

    def test_datetime_field_encrypted(self) -> None:
        plaintext = timezone.now()

        model = TestModel()
        model.datetime = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("datetime", model.id)

        # Django's normal date serialization format
        assert re.search(r"^\d\d\d\d-\d\d-\d\d", ciphertext) is None

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.datetime == plaintext

        plaintext = "text"
        model.datetime = plaintext
        model.full_clean()

        with pytest.raises(ValidationError):
            model.save()

    def test_integer_field_encrypted(self) -> None:
        plaintext = 42

        model = TestModel()
        model.integer = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("integer", model.id)

        assert plaintext != ciphertext
        assert plaintext != str(ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.integer == plaintext

        # "IntegerField": (-2147483648, 2147483647)
        plaintext = 2147483648
        model.integer = plaintext

        with pytest.raises(ValidationError):
            model.full_clean()

        plaintext = "text"
        model.integer = plaintext

        with pytest.raises(TypeError):
            model.full_clean()

    def test_date_field_encrypted(self) -> None:
        plaintext = timezone.now().date()

        model = TestModel()
        model.date = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("date", model.id)
        fresh_model = TestModel.objects.get(id=model.id)

        assert ciphertext != plaintext.isoformat()
        assert fresh_model.date == plaintext

        plaintext = "text"
        model.date = plaintext
        model.full_clean()

        with pytest.raises(ValidationError):
            model.save()

    def test_float_field_encrypted(self) -> None:
        plaintext = 42.44

        model = TestModel()
        model.floating = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("floating", model.id)

        assert plaintext != ciphertext
        assert plaintext != str(ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.floating == plaintext

        plaintext = "text"
        model.floating = plaintext
        model.full_clean()

        with pytest.raises(ValueError):
            model.save()

    def test_email_field_encrypted(self) -> None:
        plaintext = "test@gmail.com"

        model = TestModel()
        model.email = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("email", model.id)

        assert plaintext != ciphertext
        assert "aron" not in ciphertext

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.email == plaintext

        plaintext = "text"
        model.email = plaintext

        with pytest.raises(ValidationError):
            model.full_clean()

    def test_boolean_field_encrypted(self) -> None:
        plaintext = True

        model = TestModel()
        model.boolean = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("boolean", model.id)

        assert plaintext != ciphertext
        assert ciphertext is not True
        assert ciphertext != "True"
        assert ciphertext != "true"
        assert ciphertext != "1"
        assert ciphertext != 1
        assert not isinstance(ciphertext, bool)

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.boolean == plaintext

        plaintext = "text"
        model.boolean = plaintext
        model.full_clean()

        with pytest.raises(ValidationError):
            model.save()

    def test_json_field_encrypted(self) -> None:
        dict_values = {
            "key": "value",
            "list": ["nested", {"key": "val"}],
            "nested": {"child": "sibling"},
        }

        model = TestModel()
        model.json = dict_values
        model.full_clean()
        model.save()

        ciphertext = json.loads(self.get_db_value("json", model.id))

        assert dict_values != ciphertext

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.json == dict_values

    def test_json_field_retains_keys(self) -> None:
        plain_value = {"key": "value", "another_key": "some value"}

        model = TestModel()
        model.json = plain_value
        model.full_clean()
        model.save()

        ciphertext = json.loads(self.get_db_value("json", model.id))

        assert plain_value.keys() == ciphertext.keys()


class RotatedSaltTestCase(TestCase):
    @classmethod
    @override_settings(SALT_KEY=["abcdefghijklmnopqrstuvwxyz0123456789"])
    def setUpTestData(cls) -> None:
        """Create the initial record using the old salt"""
        cls.original = TestModel.objects.create(text="Oh hi test reader")

    @override_settings(SALT_KEY=["newkeyhere", "abcdefghijklmnopqrstuvwxyz0123456789"])
    def test_rotated_salt(self) -> None:
        """Change the salt, keep the old one as the last in the list for reading"""
        plaintext = "Oh hi test reader"
        model = TestModel()
        model.text = plaintext
        model.save()

        ciphertext = FieldTest.get_db_value(self, "text", model.id)

        assert plaintext != ciphertext
        assert "test" not in ciphertext

        fresh_model = TestModel.objects.get(id=model.id)
        assert fresh_model.text == plaintext

        old_record = TestModel.objects.get(id=self.original.id)
        assert fresh_model.text == old_record.text

        assert ciphertext != FieldTest.get_db_value(self, "text", self.original.pk)
