#!/usr/bin/python3
"""
Defines unittests for models/engine/file_storage.py.
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_noargs(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_witharg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_isprivate_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_isprivate_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def teststorage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFile_Storage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

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
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_witharg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        base_m = BaseModel()
        user = User()
        estado = State()
        loc = Place()
        ciudad = City()
        amnty = Amenity()
        resena = Review()
        models.storage.new(base_m)
        models.storage.new(user)
        models.storage.new(estado)
        models.storage.new(loc)
        models.storage.new(ciudad)
        models.storage.new(amnty)
        models.storage.new(resena)
        self.assertIn("BaseModel." + base_m.id, models.storage.all().keys())
        self.assertIn(base_m, models.storage.all().values())
        self.assertIn("User." + user.id, models.storage.all().keys())
        self.assertIn(user, models.storage.all().values())
        self.assertIn("State." + estado.id, models.storage.all().keys())
        self.assertIn(estado, models.storage.all().values())
        self.assertIn("Place." + loc.id, models.storage.all().keys())
        self.assertIn(loc, models.storage.all().values())
        self.assertIn("City." + ciudad.id, models.storage.all().keys())
        self.assertIn(ciudad, models.storage.all().values())
        self.assertIn("Amenity." + amnty.id, models.storage.all().keys())
        self.assertIn(amnty, models.storage.all().values())
        self.assertIn("Review." + resena.id, models.storage.all().keys())
        self.assertIn(resena, models.storage.all().values())

    def test_new_withargs(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_new_withNone(self):
        with self.assertRaises(AttributeError):
            models.storage.new(None)

    def test_save(self):
        base_m = BaseModel()
        user = User()
        estado = State()
        loc = Place()
        ciudad = City()
        amnty = Amenity()
        resena = Review()
        models.storage.new(base_m)
        models.storage.new(user)
        models.storage.new(estado)
        models.storage.new(loc)
        models.storage.new(ciudad)
        models.storage.new(amnty)
        models.storage.new(resena)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as file:
            save_text = file.read()
            self.assertIn("BaseModel." + base_m.id, save_text)
            self.assertIn("User." + user.id, save_text)
            self.assertIn("State." + estado.id, save_text)
            self.assertIn("Place." + loc.id, save_text)
            self.assertIn("City." + ciudad.id, save_text)
            self.assertIn("Amenity." + amnty.id, save_text)
            self.assertIn("Review." + resena.id, save_text)

    def test_save_witharg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        base_m = BaseModel()
        user = User()
        estado = State()
        loc = Place()
        ciudad = City()
        amnty = Amenity()
        resena = Review()
        models.storage.new(base_m)
        models.storage.new(user)
        models.storage.new(estado)
        models.storage.new(loc)
        models.storage.new(ciudad)
        models.storage.new(amnty)
        models.storage.new(resena)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + base_m.id, objs)
        self.assertIn("User." + user.id, objs)
        self.assertIn("State." + estado.id, objs)
        self.assertIn("Place." + loc.id, objs)
        self.assertIn("City." + ciudad.id, objs)
        self.assertIn("Amenity." + amnty.id, objs)
        self.assertIn("Review." + resena.id, objs)

    def test_reload_witharg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
