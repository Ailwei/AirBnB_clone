#!/usr/bin/python3
"""Module for the command interpreter entry point."""

# Importng necessary modules
import cmd
from models.base_model import BaseModel
from models import storage
import re
import json


class HBNBCommand(cmd.Cmd):

    """Command interpreter class for HBNB."""

    prompt = "(hbnb) "  # Set the command prompt

    def default(self, argument):
        """Handle commands if no other matches."""
        # print("DEF:::", argumenmt)
        self._precmd(argument)

    def _precmd(self, argument):
        """Intercept commands to test for class.syntax()"""
        # print("PRECMD:::", argument)
        match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", argument)
        if not match:
            return argument
        classname = match.group(1)
        method = match.group(2)
        args = match.group(3)
        match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_uid_and_args:
            uid = match_uid_and_args.group(1)
            attr_or_dict = match_uid_and_args.group(2)
        else:
            uid = args
            attr_or_dict = False

        attr_and_value = ""
        if method == "update" and attr_or_dict:
            match_dict = re.search('^({.*})$', attr_or_dict)
            if match_dict:
                self.update_dict(classname, uid, match_dict.group(1))
                return ""
            match_attr_and_value = re.search(
                '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
            if match_attr_and_value:
                attr_and_value = (match_attr_and_value.group(
                    1) or "") + " " + (match_attr_and_value.group(2) or "")
        command = method + " " + classname + " " + uid + " " + attr_and_value
        self.onecmd(command)
        return command

    def update_dict(self, classname, uid, s_dict):
        """Helper method for update() with a dictionary."""
        s = s_dict.replace("'", '"')
        d = json.loads(s)
        if not classname:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            else:
                attributes = storage.attributes()[classname]
                for attribute, value in d.items():
                    if attribute in attributes:
                        value = attributes[attribute](value)
                    setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()

    def do_EOF(self, argument):
        """Handle End Of File character."""
        print()
        return True

    def do_quit(self, argument):
        """Exit the program."""
        return True

    def emptyline(self):
        """Do nothing on ENTER."""
        pass

    def do_create(self, argument):
        """Create an instance."""
        if argument == "" or argument is None:
            print("** class name missing **")
        elif argument not in storage.classes():
            print("** class doesn't exist **")
        else:
            create_inst = storage.classes()[argument]()
            create_inst.save()
            print(create_inst.id)

    def do_show(self, argument):
        """Print the string representation of an instance."""
        if argument == "" or argument is None:
            print("** class name missing **")
        else:
            line = argument.split(' ')
            if line[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(line) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(line[0], line[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, argument):
        """Delete an instance based on the class name and id."""
        if argument == "" or argument is None:
            print("** class name missing **")
        else:
            line = argument.split(' ')
            if line[0] not in storage.classes():
                print("** class doesn't exist **")
            elif len(line) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(line[0], line[1])
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, argument):
        """Print string representation of all instances."""
        if argument != "":
            line = argument.split(' ')
            if line[0] not in storage.classes():
                print("** class doesn't exist **")
            else:
                no_list = [str(obj) for key, obj in storage.all().items()
                      if type(obj).__name__ == line[0]]
                print(no_list)
        else:
            create_list = [str(obj) for key, obj in storage.all().items()]
            print(create_list)

    def do_count(self, argument):
        """Count the instances of a class."""
        line = argument.split(' ')
        if not line[0]:
            print("** class name missing **")
        elif line[0] not in storage.classes():
            print("** class doesn't exist **")
        else:
            class_match = [
                k for k in storage.all() if k.startswith(
                    line[0] + '.')]
            print(len(class_match))

    def do_update(self, argument):
        """Update an instance by adding or updating attribute."""
        if argument == "" or argument is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, argument)
        classname = match.group(1)
        uid = match.group(2)
        attribute = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif classname not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(classname, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attribute:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:

                cast = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        cast = float
                    else:
                        cast = int
                else:
                    value = value.replace('"', '')
                attributes = storage.attributes()[classname]
                if attribute in attributes:
                    value = attributes[attribute](value)
                elif cast:
                    try:
                        value = cast(value)
                    except ValueError:
                        pass  # fine, stay a string then
                setattr(storage.all()[key], attribute, value)
                storage.all()[key].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()  # Run the command loop

