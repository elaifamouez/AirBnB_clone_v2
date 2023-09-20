#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""

import os

variable_name = "HBNB_TYPE_STORAGE"
env_value = os.environ.get(variable_name)

if env_value == "db":
    from models.engine.db_storage import DBStorage

    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage

    storage = FileStorage()
storage.reload()
