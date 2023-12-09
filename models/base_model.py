#!/usr/bin/python3
"""This script defines the base model class"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """BaseModel serves as the foundation for other classes"""

    def __init__(self, *args, **kwargs):
        """Initializes instance attributes based on arguments

        Args:
            - *args: List of arguments
            - **kwargs: Dictionary of key-value arguments
        """
        

        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f")
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f")
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """Returns the official string representation of the instance"""

        return "[{}] ({}) {}".\
            format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute 'updated_at'"""

        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys and values from __dict__"""

        the_dict = self.__dict__.copy()
        the_dict["__class__"] = type(self).__name__
        the_dict["created_at"] = the_dict["created_at"].isoformat()
        the_dict["updated_at"] = the_dict["updated_at"].isoformat()
        return the_dict
