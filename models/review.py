#!/usr/bin/python3
"""Module for the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """This is the Review class that inherits from BaseModel."""
    place_id = ""
    user_id = ""
    text = ""
