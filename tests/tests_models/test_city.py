#!/usr/bin/python3
"""
Defines unittests for models/city.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCityInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_noargs_instantiates(self):
        self.assertEqual(City, type(City()))

    def testnew_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_ispublic_class_attribute(self):
        citi = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(citi))
        self.assertNotIn("state_id", citi.__dict__)

    def test_name_ispublic_class_attribute(self):
        citi = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(citi))
        self.assertNotIn("name", citi.__dict__)

    def test_twocities_unique_ids(self):
        citi1 = City()
        citi2 = City()
        self.assertNotEqual(citi1.id, citi2.id)

    def test_twocities_different_created_at(self):
        citi1 = City()
        sleep(0.05)
        citi2 = City()
        self.assertLess(citi1.created_at, citi2.created_at)

    def test_twocities_different_updated_at(self):
        citi1 = City()
        sleep(0.05)
        citi2 = City()
        self.assertLess(citi1.updated_at, citi2.updated_at)

    def teststr_representation(self):
        fecha = datetime.today()
        fecha_repr = repr(fecha)
        citi = City()
        citi.id = "123456"
        citi.created_at = citi.updated_at = fecha
        citistr = citi.__str__()
        self.assertIn("[City] (123456)", citistr)
        self.assertIn("'id': '123456'", citistr)
        self.assertIn("'created_at': " + fecha_repr, citistr)
        self.assertIn("'updated_at': " + fecha_repr, citistr)

    def testargs_unused(self):
        citi = City(None)
        self.assertNotIn(None, citi.__dict__.values())

    def test_instantiation_withkwargs(self):
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        citi = City(id="345", created_at=fecha_iso, updated_at=fecha_iso)
        self.assertEqual(citi.id, "345")
        self.assertEqual(citi.created_at, fecha)
        self.assertEqual(citi.updated_at, fecha)

    def test_instantiation_withNone_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCitySave(unittest.TestCase):
    """Unittests for testing save method of the City class."""

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

    def testone_save(self):
        citi = City()
        sleep(0.05)
        first_updated_at = citi.updated_at
        citi.save()
        self.assertLess(first_updated_at, citi.updated_at)

    def testtwo_saves(self):
        citi = City()
        sleep(0.05)
        first_updated_at = citi.updated_at
        citi.save()
        second_updated_at = citi.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        citi.save()
        self.assertLess(second_updated_at, citi.updated_at)

    def test_savewith_arg(self):
        citi = City()
        with self.assertRaises(TypeError):
            citi.save(None)

    def test_saveupdates_file(self):
        citi = City()
        citi.save()
        citiid = "City." + citi.id
        with open("file.json", "r") as f:
            self.assertIn(citiid, f.read())


class TestCityToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_todict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_todict_contains_correct_keys(self):
        citi = City()
        self.assertIn("id", citi.to_dict())
        self.assertIn("created_at", citi.to_dict())
        self.assertIn("updated_at", citi.to_dict())
        self.assertIn("__class__", citi.to_dict())

    def test_todict_contains_added_attributes(self):
        citi = City()
        citi.middle_name = "Holberton"
        citi.my_number = 98
        self.assertEqual("Holberton", citi.middle_name)
        self.assertIn("my_number", citi.to_dict())

    def test_todict_datetime_attributes_are_strs(self):
        citi = City()
        citi_dict = citi.to_dict()
        self.assertEqual(str, type(citi_dict["id"]))
        self.assertEqual(str, type(citi_dict["created_at"]))
        self.assertEqual(str, type(citi_dict["updated_at"]))

    def test_todict_output(self):
        fecha = datetime.today()
        citi = City()
        citi.id = "123456"
        citi.created_at = citi.updated_at = fecha
        this_dict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': fecha.isoformat(),
            'updated_at': fecha.isoformat(),
        }
        self.assertDictEqual(citi.to_dict(), this_dict)

    def test_contrast_todict_dunder_dict(self):
        citi = City()
        self.assertNotEqual(citi.to_dict(), citi.__dict__)

    def test_todict_with_arg(self):
        citi = City()
        with self.assertRaises(TypeError):
            citi.to_dict(None)


if __name__ == "__main__":
    unittest.main()
