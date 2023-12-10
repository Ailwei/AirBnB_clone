#!/usr/bin/python3
"""
Defines unittests for models/place.py
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlaceInstantiation(unittest.TestCase):
    """Unit tests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(loc))
        self.assertNotIn("city_id", loc.__dict__)

    def test_user_id_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(loc))
        self.assertNotIn("user_id", loc.__dict__)

    def test_name_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(loc))
        self.assertNotIn("name", loc.__dict__)

    def test_description_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(loc))
        self.assertNotIn("description", loc.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(loc))
        self.assertNotIn("number_rooms", loc.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(loc))
        self.assertNotIn("number_bathrooms", loc.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(loc))
        self.assertNotIn("max_guest", loc.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(loc))
        self.assertNotIn("price_by_night", loc.__dict__)

    def test_latitude_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(loc))
        self.assertNotIn("latitude", loc.__dict__)

    def test_longitude_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(loc))
        self.assertNotIn("longitude", loc.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        loc = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(loc))
        self.assertNotIn("amenity_ids", loc.__dict__)

    def test_two_places_unique_ids(self):
        loc1 = Place()
        loc2 = Place()
        self.assertNotEqual(loc1.id, loc2.id)

    def test_two_places_different_created_at(self):
        loc1 = Place()
        sleep(0.05)
        loc2 = Place()
        self.assertLess(loc1.created_at, loc2.created_at)

    def test_twoplaces_different_updated_at(self):
        loc1 = Place()
        sleep(0.05)
        loc2 = Place()
        self.assertLess(loc1.updated_at, loc2.updated_at)

    def test_str_representation(self):
        fecha = datetime.today()
        fecha_repr = repr(fecha)
        loc = Place()
        loc.id = "123456"
        loc.created_at = loc.updated_at = fecha
        loc_str = loc.__str__()
        self.assertIn("[Place] (123456)", loc_str)
        self.assertIn("'id': '123456'", loc_str)
        self.assertIn("'created_at': " + fecha_repr, loc_str)
        self.assertIn("'updated_at': " + fecha_repr, loc_str)

    def test_args_unused(self):
        loc = Place(None)
        self.assertNotIn(None, loc.__dict__.values())

    def test_instantiation_with_kwargs(self):
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        loc = Place(id="345", created_at=fecha_iso, updated_at=fecha_iso)
        self.assertEqual(fecha.id, "345")
        self.assertEqual(loc.created_at, fecha)
        self.assertEqual(loc.updated_at, fecha)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlaceSave(unittest.TestCase):
    """Unit tests for testing save method of the Place class."""

    @classmethod
    def setUp(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_onesave(self):
        loc = Place()
        sleep(0.05)
        first_updated_at = loc.updated_at
        loc.save()
        self.assertLess(first_updated_at, loc.updated_at)

    def test_twosaves(self):
        loc = Place()
        sleep(0.05)
        first_updated_at = loc.updated_at
        loc.save()
        second_updated_at = loc.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        loc.save()
        self.assertLess(second_updated_at, loco.updated_at)

    def test_savewith_arg(self):
        loc = Place()
        with self.assertRaises(TypeError):
            loc.save(None)

    def test_saveupdates_file(self):
        loc = Place()
        loc.save()
        place_id = "Place." + loc.id
        with open("file.json", "r") as f:
            self.assertIn(place_id, f.read())


class TestPlaceToDict(unittest.TestCase):
    """Unit tests for testing to_dict method of the Place class."""

    def test_todict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_todict_contains_correct_keys(self):
        loc = Place()
        self.assertIn("id", loc.to_dict())
        self.assertIn("created_at", loc.to_dict())
        self.assertIn("updated_at", loc.to_dict())
        self.assertIn("__class__", loc.to_dict())

    def test_todict_contains_added_attributes(self):
        loc = Place()
        loc.middle_name = "Holberton"
        loc.my_number = 98
        self.assertEqual("Holberton", loc.middle_name)
        self.assertIn("my_number", loc.to_dict())

    def test_todict_datetime_attributes_are_strs(self):
        loc = Place()
        place_dict = loc.to_dict()
        self.assertEqual(str, type(place_dict["id"]))
        self.assertEqual(str, type(place_dict["created_at"]))
        self.assertEqual(str, type(place_dict["updated_at"]))

    def test_todict_output(self):
        fecha = datetime.today()
        loc = Place()
        loc.id = "123456"
        loc.created_at = loc.updated_at = fecha
        this_dict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': fecha.isoformat(),
            'updated_at': fecha.isoformat(),
        }
        self.assertDictEqual(loc.to_dict(), this_dict)

    def test_contrast_todict_dunder_dict(self):
        loc = Place()
        self.assertNotEqual(loc.to_dict(), loc.__dict__)

    def test_todict_with_arg(self):
        loc = Place()
        with self.assertRaises(TypeError):
            loc.to_dict(None)


if __name__ == "__main__":
    unittest.main()
