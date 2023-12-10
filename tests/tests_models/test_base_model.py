#!/usr/bin/python3
"""
Defines unittests for models/base_model.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_instantiation(unittest.TestCase):
    """Unit tests for testing instantiation of the BaseModel class."""

    def test_noargs_instantiates(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_inobjects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_twomodels_unique_ids(self):
        base_m1 = BaseModel()
        base_m2 = BaseModel()
        self.assertNotEqual(base_m1.id, base_m2.id)

    def test_twomodels_different_created_at(self):
        base_m1 = BaseModel()
        sleep(0.05)
        base_m2 = BaseModel()
        self.assertLess(base_m1.created_at, base_m2.created_at)

    def test_twomodels_different_updated_at(self):
        base_m1 = BaseModel()
        sleep(0.05)
        base_m2 = BaseModel()
        self.assertLess(base_m1.updated_at, base_m2.updated_at)

    def test_strrepresentation(self):
        fecha = datetime.today()
        fecha_repr = repr(fecha)
        base_m = BaseModel()
        base_m.id = "123456"
        base_m.created_at = base_m.updated_at = fecha
        base_m_str = base_m.__str__()
        self.assertIn("[BaseModel] (123456)", base_m_str)
        self.assertIn("'id': '123456'", base_m_str)
        self.assertIn("'created_at': " + fecha_repr, base_m_str)
        self.assertIn("'updated_at': " + fecha_repr, base_m_str)

    def test_argsunused(self):
        base_m = BaseModel(None)
        self.assertNotIn(None, base_m.__dict__.values())

    def test_instantiation_withkwargs(self):
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        base_m = BaseModel(
                id="345",
                created_at=fecha_iso,
                updated_at=fecha_iso
                )
        self.assertEqual(base_m.id, "345")
        self.assertEqual(base_m.created_at, fecha)
        self.assertEqual(base_m.updated_at, fecha)

    def test_instantiation_withNone_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instantiation_withargs_and_kwargs(self):
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        base_m = BaseModel(
                "12", id="345",
                created_at=fecha_iso,
                updated_at=fecha_iso
                )
        self.assertEqual(base_m.id, "345")
        self.assertEqual(base_m.created_at, fecha)
        self.assertEqual(base_m.updated_at, fecha)


class TestBaseModel_save(unittest.TestCase):
    """Unit tests for testing save method of the BaseModel class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_onesave(self):
        base_m = BaseModel()
        sleep(0.05)
        first_updated_at = base_m.updated_at
        base_m.save()
        self.assertLess(first_updated_at, base_m.updated_at)

    def test_twosaves(self):
        base_m = BaseModel()
        sleep(0.05)
        first_updated_at = base_m.updated_at
        base_m.save()
        second_updated_at = base_m.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base_m.save()
        self.assertLess(second_updated_at, base_m.updated_at)

    def test_save_witharg(self):
        base_m = BaseModel()
        with self.assertRaises(TypeError):
            base_m.save(None)

    def testsave_updates_file(self):
        base_m = BaseModel()
        base_m.save()
        base_m_id = "BaseModel." + base_m.id
        with open("file.json", "r") as f:
            self.assertIn(base_m_id, f.read())


class TestBaseModel_todict(unittest.TestCase):
    """Unit tests for testing to_dict method of the BaseModel class."""

    def test_todict_type(self):
        base_m = BaseModel()
        self.assertTrue(dict, type(base_m.to_dict()))

    def test_todict_contains_correct_keys(self):
        base_m = BaseModel()
        self.assertIn("id", base_m.to_dict())
        self.assertIn("created_at", base_m.to_dict())
        self.assertIn("updated_at", base_m.to_dict())
        self.assertIn("__class__", base_m.to_dict())

    def test_todict_contains_added_attributes(self):
        base_m = BaseModel()
        base_m.name = "Holberton"
        base_m.my_number = 98
        self.assertIn("name", base_m.to_dict())
        self.assertIn("my_number", base_m.to_dict())

    def test_todict_datetime_attributes_are_strs(self):
        base_m = BaseModel()
        base_m_dict = base_m.to_dict()
        self.assertEqual(str, type(base_m_dict["created_at"]))
        self.assertEqual(str, type(base_m_dict["updated_at"]))

    def test_todict_output(self):
        fecha = datetime.today()
        base_m = BaseModel()
        base_m.id = "123456"
        base_m.created_at = base_m.updated_at = fecha
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': fecha.isoformat(),
            'updated_at': fecha.isoformat()
        }
        self.assertDictEqual(base_m.to_dict(), tdict)

    def test_contrast_todict_dunder_dict(self):
        base_m = BaseModel()
        self.assertNotEqual(base_m.to_dict(), base_m.__dict__)

    def test_todict_with_arg(self):
        base_m = BaseModel()
        with self.assertRaises(TypeError):
            base_m.to_dict(None)


if __name__ == "__main__":
    unittest.main()
