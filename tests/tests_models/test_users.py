#!/usr/bin/python3
"""Defines unittests for models/user.py.

Unittest classes:
    TestUserInstantiation
    TestUserSave
    TestUserToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUserInstantiation(unittest.TestCase):
    """Test instantiation of the User class."""

    def test_instantiation_with_no_arguments(self):
        """Test User instantiation with no arguments."""
        self.assertEqual(User, type(User()))

    def test_new_instances_stored_object(self):
        """Test that a new User instance is stored in objects."""
        self.assertIn(User(), models.storage.all().values())

    def test_id_ispublic_string(self):
        """Test that the id attribute is a public string."""
        self.assertEqual(str, type(User().id))

    def test_created_at_ispublic_datetime(self):
        """Test that created_at is a public datetime attribute."""
        self.assertEqual(datetime, type(User().created_at))

    def test_updated_at_ispublic_datetime(self):
        """Test that updated_at is a public datetime attribute."""
        self.assertEqual(datetime, type(User().updated_at))

    def test_email_ispublic_string(self):
        """Test that email is a public string attribute."""
        self.assertEqual(str, type(User.email))

    def test_pwd_ispublic_string(self):
        """Test that password is a public string attribute."""
        self.assertEqual(str, type(User.password))

    def test_firstname_is_public_string(self):
        """Test that first_name is a public string attribute."""
        self.assertEqual(str, type(User.first_name))

    def test_lastname_is_public_string(self):
        """Test that last_name is a public string attribute."""
        self.assertEqual(str, type(User.last_name))

    def test_uniqueid_for_two_users(self):
        """Test that two users have unique ids."""
        user_one = User()
        user_two = User()
        self.assertNotEqual(user_one.id, user_two.id)

    def test_different_createdat_for_two_users(self):
        """Test that two users have different created_at values."""
        user_one = User()
        sleep(0.05)
        user_two = User()
        self.assertLess(user_one.created_at, user_two.created_at)

    def test_different_updatedat_for_two_users(self):
        """Test that two users have different updated_at values."""
        user_one = User()
        sleep(0.05)
        user_two = User()
        self.assertLess(user_one.updated_at, user_two.updated_at)

    def test_string_representation(self):
        """Test the string representation of a User instance."""
        fecha = datetime.today()
        fecha_repr = repr(fecha)
        account = User()
        account.id = "245678"
        account.created_at = account.updated_at = fecha
        user_str = account.__str__()
        self.assertIn("[User] (345)", user_str)
        self.assertIn("'id': '13579'", user_str)
        self.assertIn("'created_at': " + fecha_repr, user_str)
        self.assertIn("'updated_at': " + fecha_repr, user_str)

    def test_unusedargs_donot_affect_instance(self):
        """Test that unused arguments do not affect the instance."""
        account = User(None)
        self.assertNotIn(None, account.__dict__.values())

    def test_instantiation_with_kwargs(self):
        """Test instantiation with keyword arguments."""
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        user = User(id="345", created_at=fecha_iso, updated_at=fecha_iso)
        self.assertEqual(user.id, "345")
        self.assertEqual(user.created_at, fecha)
        self.assertEqual(user.updated_at, fecha)

    def test_instantiation_withnone_kwargs_raises_typeerror(self):
        """Test that instantiation with None kwargs raises TypeError."""
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUserSave(unittest.TestCase):
    """Test the save method of the User class."""

    @classmethod
    def setUp(cls):
        """Set up for testing save method."""
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        """Tear down after testing save method."""
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_onesave_updates_updatedat(self):
        """Test that save updates the updated_at attribute."""
        account = User()
        sleep(0.05)
        first_updated_at = account.updated_at
        account.save()
        self.assertLess(first_updated_at, account.updated_at)

    def test_twosaves_updates_updatedat(self):
        """Test that two consecutive saves update the updated_at attribute."""
        account = User()
        sleep(0.05)
        first_updated_at = account.updated_at
        account.save()
        second_updated_at = account.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        account.save()
        self.assertLess(second_updated_at, account.updated_at)

    def test_save_witharg_raises_type_error(self):
        """Test that save with an argument raises TypeError."""
        account = User()
        with self.assertRaises(TypeError):
            account.save(None)

    def test_saveupdates_file(self):
        """Test that save updates the file."""
        account = User()
        account.save()
        user_id = "User." + account.id
        with open("file.json", "r") as file:
            self.assertIn(user_id, file.read())


class TestUser_ToDict(unittest.TestCase):
    """Test the to_dict method of the User class."""

    def test_to_dict_returns_dictionary(self):
        """Test that to_dict returns a dictionary."""
        self.assertTrue(dict, type(User().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        """Test that to_dict contains the correct keys."""
        account = User()
        self.assertIn("id", account.to_dict())
        self.assertIn("created_at", account.to_dict())
        self.assertIn("updated_at", account.to_dict())
        self.assertIn("__class__", account.to_dict())

    def test_to_dict_contains_added_attributes(self):
        """Test that to_dict contains added attributes."""
        account = User()
        account.middle_name = "Holberton"
        account.my_number = 98
        self.assertEqual("Holberton", account.middle_name)
        self.assertIn("my_number", account.to_dict())

    def test_todict_datetime_attributes_are_strings(self):
        """Test that to_dict datetime attributes are strings."""
        account = User()
        users_dict = account.to_dict()
        self.assertEqual(str, type(users_dict["id"]))
        self.assertEqual(str, type(users_dict["created_at"]))
        self.assertEqual(str, type(users_dict["updated_at"]))

    def test_todict_output(self):
        """Test the output of to_dict."""
        fecha = datetime.today()
        account = User()
        account.id = "123456"
        account.created_at = account.updated_at = fecha
        expected_dicts = {
            'id': '123456',
            '__class__': 'User',
            'created_at': fecha.isoformat(),
            'updated_at': fecha.isoformat(),
        }
        self.assertDictEqual(account.to_dict(), expected_dicts)

    def test_contrast_todict_with_dunderdict(self):
        """Test that to_dict is different from __dict__."""
        account = User()
        self.assertNotEqual(account.to_dict(), account.__dict__)

    def test_todict_witharg_raises_type_error(self):
        """Test that to_dict with an argument raises TypeError."""
        account = User()
        with self.assertRaises(TypeError):
            account.to_dict(None)


if __name__ == "__main__":
    unittest.main()
