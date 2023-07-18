import json
import re

from django.db import connection
from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.exceptions import ValidationError

from .models import TestModel


class FieldTest(TestCase):
    def get_db_value(self, field, model_id):
        cursor = connection.cursor()
        cursor.execute(
            "select {0} "
            "from package_test_testmodel "
            "where id = {1};".format(field, model_id)
        )
        return cursor.fetchone()[0]

    def test_char_field_encrypted(self):
        plaintext = "Oh hi, test reader!"

        model = TestModel()
        model.char = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("char", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertTrue("test" not in ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.char, plaintext)

    def test_text_field_encrypted(self):
        plaintext = "Oh hi, test reader!" * 10

        model = TestModel()
        model.text = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("text", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertTrue("test" not in ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.text, plaintext)

    def test_datetime_field_encrypted(self):
        plaintext = timezone.now()

        model = TestModel()
        model.datetime = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("datetime", model.id)

        # Django's normal date serialization format
        self.assertTrue(re.search("^\d\d\d\d-\d\d-\d\d", ciphertext) is None)

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.datetime, plaintext)

        plaintext = "text"

        with self.assertRaises(ValidationError):
            model.datetime = plaintext
            model.full_clean()
            model.save()

    def test_integer_field_encrypted(self):
        plaintext = 42

        model = TestModel()
        model.integer = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("integer", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertNotEqual(plaintext, str(ciphertext))

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.integer, plaintext)

        # "IntegerField": (-2147483648, 2147483647)
        plaintext = 2147483648

        with self.assertRaises(ValidationError):
            model.integer = plaintext
            model.full_clean()
            model.save()

        plaintext = "text"

        with self.assertRaises(TypeError):
            model.integer = plaintext
            model.full_clean()
            model.save()

    def test_date_field_encrypted(self):
        plaintext = timezone.now().date()

        model = TestModel()
        model.date = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("date", model.id)
        fresh_model = TestModel.objects.get(id=model.id)

        self.assertNotEqual(ciphertext, plaintext.isoformat())
        self.assertEqual(fresh_model.date, plaintext)

        plaintext = "text"

        with self.assertRaises(ValidationError):
            model.date = plaintext
            model.full_clean()
            model.save()

    def test_float_field_encrypted(self):
        plaintext = 42.44

        model = TestModel()
        model.floating = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("floating", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertNotEqual(plaintext, str(ciphertext))

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.floating, plaintext)

        plaintext = "text"

        with self.assertRaises(ValueError):
            model.floating = plaintext
            model.full_clean()
            model.save()

    def test_email_field_encrypted(self):
        plaintext = "test@gmail.com"

        model = TestModel()
        model.email = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("email", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertTrue("aron" not in ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.email, plaintext)

        plaintext = "text"

        with self.assertRaises(ValidationError):
            model.email = plaintext
            model.full_clean()
            model.save()

    def test_boolean_field_encrypted(self):
        plaintext = True

        model = TestModel()
        model.boolean = plaintext
        model.full_clean()
        model.save()

        ciphertext = self.get_db_value("boolean", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertNotEqual(True, ciphertext)
        self.assertNotEqual("True", ciphertext)
        self.assertNotEqual("true", ciphertext)
        self.assertNotEqual("1", ciphertext)
        self.assertNotEqual(1, ciphertext)
        self.assertTrue(not isinstance(ciphertext, bool))

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.boolean, plaintext)

        plaintext = "text"

        with self.assertRaises(ValidationError):
            model.boolean = plaintext
            model.full_clean()
            model.save()

    def test_json_field_encrypted(self):
        dict_values = {"key": "value", "list": ["nested", {"key": "val"}], "nested": {"child": "sibling"}}

        model = TestModel()
        model.json = dict_values
        model.full_clean()
        model.save()

        ciphertext = json.loads(self.get_db_value("json", model.id))


        self.assertNotEqual(dict_values, ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.json, dict_values)

    def test_json_field_retains_keys(self):
        plain_value = {"key": "value", "another_key": "some value"}
        
        model = TestModel()
        model.json = plain_value
        model.full_clean()
        model.save()

        ciphertext = json.loads(self.get_db_value("json", model.id))

        self.assertEqual(plain_value.keys(), ciphertext.keys())


class RotatedSaltTestCase(TestCase):
    @classmethod
    @override_settings(SALT_KEY=["abcdefghijklmnopqrstuvwxyz0123456789"])
    def setUpTestData(cls):
        """Create the initial record using the old salt"""
        cls.original = TestModel.objects.create(text="Oh hi test reader")

    @override_settings(SALT_KEY=["newkeyhere", "abcdefghijklmnopqrstuvwxyz0123456789"])
    def test_rotated_salt(self):
        """Change the salt, keep the old one as the last in the list for reading"""
        plaintext = "Oh hi test reader"
        model = TestModel()
        model.text = plaintext
        model.save()

        ciphertext = FieldTest.get_db_value(self, "text", model.id)

        self.assertNotEqual(plaintext, ciphertext)
        self.assertTrue("test" not in ciphertext)

        fresh_model = TestModel.objects.get(id=model.id)
        self.assertEqual(fresh_model.text, plaintext)

        old_record = TestModel.objects.get(id=self.original.id)
        self.assertEqual(fresh_model.text, old_record.text)

        self.assertNotEqual(
            ciphertext, FieldTest.get_db_value(self, "text", self.original.pk)
        )
