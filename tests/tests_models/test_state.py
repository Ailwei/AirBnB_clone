#!/usr/bin/python3
"""
Defines unittests for models/state.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestStateInstantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_instantiation_with_noargs(self):
        self.assertEqual(State, type(State()))

    def test_newinstance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_ispublic_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_ispublic_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_ispublic_class_attribute(self):
        state_ = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(state_))
        self.assertNotIn("name", state_.__dict__)

    def test_uniqueids_for_two_states(self):
        state_one = State()
        state_two = State()
        self.assertNotEqual(state_one.id, state_two.id)

    def test_different_created_at_for_two_states(self):
        state_one = State()
        sleep(0.05)
        state_two = State()
        self.assertLess(state_one.created_at, state_two.created_at)

    def test_different_updated_at_for_two_states(self):
        state_one = State()
        sleep(0.05)
        state_two = State()
        self.assertLess(state_one.updated_at, state_two.updated_at)

    def test_strrepresentation(self):
        fecha = datetime.today()
        fecha_repr = repr(fecha)
        state_ = State()
        state_.id = "123456"
        state_.created_at = state_.updated_at = fecha
        state_str = state_.__str__()
        self.assertIn("[State] (123456)", state_str)
        self.assertIn("'id': '123456'", state_str)
        self.assertIn("'created_at': " + fecha_repr, state_str)
        self.assertIn("'updated_at': " + fecha_repr, state_str)

    def test_unused_args_donotaffect_instance(self):
        state_ = State(None)
        self.assertNotIn(None, state_.__dict__.values())

    def test_instantiation_withkwargs(self):
        fecha = datetime.today()
        fecha_iso = fecha.isoformat()
        state_ = State(id="345", created_at=fecha_iso, updated_at=fecha_iso)
        self.assertEqual(state_.id, "345")
        self.assertEqual(state_.created_at, fecha)
        self.assertEqual(state_.updated_at, fecha)

    def test_instantiation_with_Nonekwargs_raises_typeerror(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestStateSave(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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

    def testone_save_updates_updated_at(self):
        state_ = State()
        sleep(0.05)
        first_updated_at = state_.updated_at
        state_.save()
        self.assertLess(first_updated_at, state_.updated_at)

    def test_two_saves_updates_updated_at(self):
        state_ = State()
        sleep(0.05)
        first_updated_at = state_.updated_at
        state_.save()
        second_updated_at = state_.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        state_.save()
        self.assertLess(second_updated_at, state_.updated_at)

    def testsave_with_argument_raises_type_error(self):
        state_ = State()
        with self.assertRaises(TypeError):
            state_.save(None)

    def testsave_updates_file(self):
        state_ = State()
        state_.save()
        state_id = "State." + state_.id
        with open("file.json", "r") as f:
            self.assertIn(state_id, f.read())


class TestStateToDict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_todict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_todict_contains_correct_keys(self):
        state_ = State()
        self.assertIn("id", state_.to_dict())
        self.assertIn("created_at", state_.to_dict())
        self.assertIn("updated_at", state_.to_dict())
        self.assertIn("__class__", state_.to_dict())

    def test_todict_contains_added_attributes(self):
        state_ = State()
        state_.middle_name = "Holberton"
        state_.my_number = 98
        self.assertEqual("Holberton", state_.middle_name)
        self.assertIn("my_number", state_.to_dict())

    def test_todict_datetime_attributes_are_strs(self):
        state_ = State()
        state_dict = state_.to_dict()
        self.assertEqual(str, type(state_dict["id"]))
        self.assertEqual(str, type(state_dict["created_at"]))
        self.assertEqual(str, type(state_dict["updated_at"]))

    def test_todict_output(self):
        fecha = datetime.today()
        state_ = State()
        state_.id = "123456"
        state_.created_at = state_.updated_at = fecha
        expected_dictionary = {
            'id': '123456',
            '__class__': 'State',
            'created_at': fecha.isoformat(),
            'updated_at': fecha.isoformat(),
        }
        self.assertDictEqual(state_.to_dict(), expected_dictionary)

    def test_contrast_todict_with_dunder_dict(self):
        state_ = State()
        self.assertNotEqual(state_.to_dict(), state_.__dict__)

    def test_todict_with_argument_raises_type_error(self):
        state_ = State()
        with self.assertRaises(TypeError):
            state_.to_dict(None)


if __name__ == "__main__":
    unittest.main()

