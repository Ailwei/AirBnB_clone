#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestResenaInstantiation
    TestResenaSave
    TestResenaToDict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestResenaInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Resena class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        resena = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(resena))
        self.assertNotIn("place_id", resena.__dict__)

    def test_user_id_is_public_class_attribute(self):
        resena = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(resena))
        self.assertNotIn("user_id", resena.__dict__)

    def test_text_is_public_class_attribute(self):
        resena = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(resena))
        self.assertNotIn("text", resena.__dict__)

    def test_two_reviews_unique_ids(self):
        resena1 = Review()
        resena2 = Review()
        self.assertNotEqual(resena1.id, resena2.id)

    def test_two_reviews_different_created_at(self):
        resena1 = Review()
        sleep(0.05)
        resena2 = Review()
        self.assertLess(resena1.created_at, resena2.created_at)

    def test_two_reviews_different_updated_at(self):
        resena1 = Review()
        sleep(0.05)
        resena2 = Review()
        self.assertLess(resena1.updated_at, resena2.updated_at)

    def test_str_representation(self):
        fecha = datetime.today()
        fecha_repr = repr(fecha)
        resena = Review()
        resena.id = "123456"
        resena.created_at = resena.updated_at = fecha
        resena_str = resena.__str__()
        self.assertIn("[Review] (123456)", resena_str)
        self.assertIn("'id': '123456'", resena_str)
        self.assertIn("'created_at': " + fecha_repr, resena_str)
        self.assertIn("'updated_at': " + fecha_repr, resena_str)

    def test_args_unused(self):
        resena = Review(None)
        self.assertNotIn(None, resena.__dict__.values())

    def test_instantiation_with_kwargs(self):
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        resena = Review(id="345", created_at=fecha_iso, updated_at=fecha_iso)
        self.assertEqual(resena.id, "345")
        self.assertEqual(resena.created_at, fecha)
        self.assertEqual(resena.updated_at, fecha)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestResenaSave(unittest.TestCase):
    """Unittests for testing save method of the Resena class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        resena = Review()
        sleep(0.05)
        first_updated_at = resena.updated_at
        resena.save()
        self.assertLess(first_updated_at, resena.updated_at)

    def test_two_saves(self):
        resena = Review()
        sleep(0.05)
        first_updated_at = resena.updated_at
        resena.save()
        second_updated_at = resena.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        resena.save()
        self.assertLess(second_updated_at, resena.updated_at)

    def test_save_with_arg(self):
        resena = Review()
        with self.assertRaises(TypeError):
            resena.save(None)

    def test_save_updates_file(self):
        resena = Review()
        resena.save()
        resena_id = "Review." + resena.id
        with open("file.json", "r") as f:
            self.assertIn(resena_id, f.read())


class TestResenaToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the Resena class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        resena = Review()
        self.assertIn("id", resena.to_dict())
        self.assertIn("created_at", resena.to_dict())
        self.assertIn("updated_at", resena.to_dict())
        self.assertIn("__class__", resena.to_dict())

    def test_to_dict_contains_added_attributes(self):
        resena = Review()
        resena.middle_name = "Holberton"
        resena.my_number = 98
        self.assertEqual("Holberton", resena.middle_name)
        self.assertIn("my_number", resena.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        resena = Review()
        resena_dict = resena.to_dict()
        self.assertEqual(str, type(resena_dict["id"]))
        self.assertEqual(str, type(resena_dict["created_at"]))
        self.assertEqual(str, type(resena_dict["updated_at"]))

    def test_to_dict_output(self):
        fecha = datetime.today()
        resena = Review()
        resena.id = "21006"
        resena.created_at = resena.updated_at = fecha
        tdict = {
            'id': '21006',
            '__class__': 'Review',
            'created_at': fecha.isoformat(),
            'updated_at': fecha.isoformat(),
        }
        self.assertDictEqual(resena.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        resena = Review()
        self.assertNotEqual(resena.to_dict(), resena.__dict__)

    def test_to_dict_with_arg(self):
        resena = Review()
        with self.assertRaises(TypeError):
            resena.to_dict(None)


if __name__ == "__main__":
    unittest.main()

