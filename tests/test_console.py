#!/usr/bin/python3

import sys
sys.path.append(".")
import os
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch, MagicMock

class TestHBNBCommand_prompt(unittest.TestCase):
    """Unit test for testing prompting of the HBNB command."""

    def test_prompt_str(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_emptyline(self):
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", result.getvalue().strip())


class TestHBNBCommandHelp(unittest.TestCase):
    """ testing help messagez of the HBNB command interpreter."""

    def test_help_toquit(self):
        to_quit = "Quit command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(to_quit, result.getvalue().strip())

    def test_help_tocreate(self):
        to_create = ("Usage: create <class>\n        "
             "Create a new class instance and print its id.")
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(to_create, result.getvalue().strip())

    def test_help_EOF(self):
        for_EOF = "Handle End Of File character."
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(for_EOF, result.getvalue().strip())


class TestHBNBCommand_toExit(unittest.TestCase):
    """Unit tests for testing exiting from the HBNB command interpreter."""

    def test_quit_toexits(self):
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertTrue(HBNBCommand().onecmd("quit"))


    def test_EOF_exits(self):
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandi_Create(unittest.TestCase):
    """for testing create from the HBNB command."""

    @classmethod
    def set_Up(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tear_Down(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missingclass(self):
        correct_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_create_invalidclass(self):
        correct_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_create_invalid_syntax(self):
        correct_output = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct_output, result.getvalue().strip())
        correct_output = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "BaseModel.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "User.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "State.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "City.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "Amenity.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "Place.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(result.getvalue().strip()))
            test_Key = "Review.{}".format(result.getvalue().strip())
            self.assertIn(test_Key, storage.all().keys())
class TestHBNBCommandShow(unittest.TestCase):
    """testing show from the HBNB command interpreter"""

    @classmethod
    def setUp_Class(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown_Class(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missingclass(self):
        correct_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(correct_output, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_show_invalid_class(self):
        correct_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct_output, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_show_missing_id_space_nota(self):
        correct_output = "** instance id missing **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"show {class_name}"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_show_missing_id_dot_nota(self):
        correct_output = "** instance id missing **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{class_name}.show()"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_show_no_instance_foundspace_notation(self):
        correct_output = "** no instance found **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"show {class_name} 1"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_show_no_instance_found_dotnotation(self):
        correct_output = "** no instance found **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{class_name}.show(1)"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_show_objects_spacenotation(self):
        classes_to_test = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
                test_id = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                obj = storage.all()[f"{class_name}.{test_id}"]
                command = f"show {class_name} {test_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), result.getvalue().strip())

    def test_show_objects_dotnotation(self):
        classes_to_test = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
                test_id = output.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                obj = storage.all()[f"{class_name}.{test_id}"]
                command = f"{class_name}.show({test_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertEqual(obj.__str__(), result.getvalue().strip())

class TestHBNBCommandDestroy(unittest.TestCase):
    """Unit tests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_destroy_missingclass(self):
        correct_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct_output, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_destroy_invalidclass(self):
        correct_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct_output, result.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct_output, result.getvalue().strip())

    def test_destroy_id_missing_spacenotation(self):
        correct_output = "** instance id missing **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {class_name}"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_destroy_id_missing_dotnotation(self):
        correct_output = "** instance id missing **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{class_name}.destroy()"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_destroy_invalid_id_spacenotation(self):
        correct_output = "** no instance found **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"destroy {class_name} 1"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_destroy_invalid_id_dotnotation(self):
        correct_output = "** no instance found **"
        classes_to_test = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{class_name}.destroy(1)"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_destroy_objects_spacenotation(self):
        classes_to_test = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
                test_id = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                objs = storage.all()[f"{class_name}.{test_id}"]
                command = f"destroy {class_name} {test_id}"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(objs, storage.all())

    def test_destroy_objects_dotnotation(self):
        classes_to_test = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
                test_id = result.getvalue().strip()
            with patch("sys.stdout", new=StringIO()) as result:
                objs = storage.all()[f"{class_name}.{test_id}"]
                command = f"{class_name}.destroy({test_id})"
                self.assertFalse(HBNBCommand().onecmd(command))
                self.assertNotIn(objs, storage.all())

class TestHBNBCommandAll(unittest.TestCase):
    """testing 'all' from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_invalidclass(self):
        correct_output = "** class doesn't exist **"
        classes_to_test = ["MyModel", "MyModel.all()"]
        for class_name in classes_to_test:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"all {class_name}"))
                self.assertEqual(correct_output, result.getvalue().strip())

    def test_all_objects_spacenotation(self):
        classes_to_create = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        with patch("sys.stdout", new=StringIO()) as result:
            for class_name in classes_to_create:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            self.assertFalse(HBNBCommand().onecmd("all"))
            for class_name in classes_to_create:
                self.assertIn(class_name, result.getvalue().strip())

    def test_all_objects_dotnotation(self):
        classes_to_create = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]
        with patch("sys.stdout", new=StringIO()) as result:
            for class_name in classes_to_create:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            for class_name in classes_to_create:
                self.assertIn(class_name, result.getvalue().strip())

    def test_all_single_object_spacenotation(self):
        classes_to_create = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_create:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"all {class_name}"))
                self.assertIn(class_name, result.getvalue().strip())
                self.assertNotIn("BaseModel", result.getvalue().strip())

    def test_all_single_object_dotnotation(self):
        classes_to_create = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
        for class_name in classes_to_create:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            with patch("sys.stdout", new=StringIO()) as resultt:
                self.assertFalse(HBNBCommand().onecmd(f"{class_name}.all()"))
                self.assertIn(class_name, result.getvalue().strip())
                self.assertNotIn("BaseModel", result.getvalue().strip())

class TestHBNBCommandUpdate(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def assertUpdate_Output(self, cmd, expected_output):
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd(cmd))
            self.assertEqual(expected_output, result.getvalue().strip())

    def test_update_missingclass(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("update")
            self.assertEqual(result.getvalue().strip(), "Class name missing")

    def test_update_valid_int_attr_spacenotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            test_id = result.getvalue().strip()
        test_cmd = "update Place {} max_guest 98".format(test_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmd))
        test_dict = storage.all()["Place.{}".format(test_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])        

    def test_update_valid_float_attr_spacenotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            obj_id = result.getvalue().strip()

        test_cmd = "update Place {} latitude 7.2".format(obj_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmd))

        test_dict = storage.all()["Place.{}".format(obj_id)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dotnotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            obj_id  = result.getvalue().strip()
        print("Before Update:", storage.all()["Place.{}".format(obj_id)].__dict__)


        test_cmd = "Place.update({}, latitude, 7.2)".format(obj_id)
        self.assertFalse(HBNBCommand().onecmd(test_cmd))

        test_dict = storage.all()["Place.{}".format(obj_id)].__dict__
        print("After Update:", test_dict)

        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_spacenotation(self):
        test_classes = ["BaseModel", "User", "State", "City", "Place", "Amenity", "Review"]

        for class_name in test_classes:
            with patch("sys.stdout", new=StringIO()) as result:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = obj_id = result.getvalue().strip()

            test_cmd = f"update {class_name} {obj_id} "
            test_cmd += "{'attr_name': 'attr_value'}"
            HBNBCommand().onecmd(test_cmd)

            test_dict = storage.all()[f"{class_name}.{obj_id}"].__dict__
            self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dotnotation(self):
        test_classes = ["BaseModel", "User", "State", "City", "Place", "Amenity", "Review"]

        for class_name in test_classes:
            with patch("sys.stdout", new=StringIO()) as result:
                HBNBCommand().onecmd(f"create {class_name}")
                obj_id = result.getvalue().strip()

            test_cmd = f"{class_name}.update({obj_id} "
            test_cmd += "{'attr_name': 'attr_value'})"
            HBNBCommand().onecmd(test_cmd)

            test_dict = storage.all()[f"{class_name}.{obj_id}"].__dict__
            self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_spacenotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            obj_id = result.getvalue().strip()

        test_cmd = "update Place {} ".format(obj_id)
        test_cmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_cmd)

        test_dict = storage.all()["Place.{}".format(obj_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dotnotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            obj_id = result.getvalue().strip()

        test_cmd = "Place.update({}, ".format(obj_id)
        test_cmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(test_cmd)

        test_dict = storage.all()["Place.{}".format(obj_id)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_spacenotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            obj_id = result.getvalue().strip()

        test_cmd = "Place.update({}, ".format(obj_id)
        test_cmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_cmd)

        test_dict = storage.all()["Place.{}".format(obj_id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dotnotation(self):
        with patch("sys.stdout", new=StringIO()) as result:
            HBNBCommand().onecmd("create Place")
            obj_id = result.getvalue().strip()

        test_cmd = "Place.update({}, ".format(obj_id)
        test_cmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(test_cmd)

        test_dict = storage.all()["Place.{}".format(obj_id)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

class TestHBNBCommand_Count(unittest.TestCase):
    """testing count method of HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        storage._FileStorage__objects = {}

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalidC_class(self):
        with patch("sys.stdout", new=StringIO()) as result:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("** class doesn't exist **", result.getvalue().strip())

    def test_count_Object(self):
        test_classes = ["BaseModel", "User", "State", "Place", "City", "Amenity", "Review"]

        for class_name in test_classes:
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"create {class_name}"))
            
            with patch("sys.stdout", new=StringIO()) as result:
                self.assertFalse(HBNBCommand().onecmd(f"{class_name}.count()"))
                self.assertEqual("366", result.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
