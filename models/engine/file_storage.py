#!/usr/bin/python3
"""
This script encapsulates the FileStorage class for serializing and deserializing instances to/from a JSON file.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

# Dictionary mapping class names to their corresponding classes
class_map = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
             "Place": Place, "Review": Review, "State": State, "User": User}

class FileStorage:
    """
    This class handles the serialization of instances to a JSON file and the deserialization back to instances.
    """
    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects, filtered by class if specified.
        """
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Adds an object to the __objects dictionary with the key format <obj class name>.id.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes the __objects dictionary to the JSON file specified by __file_path.
        """
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict(dump="Yes")
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file to the __objects dictionary.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = class_map[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """
        Removes an object from the __objects dictionary if it exists.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Calls the reload() method to deserialize the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves an object based on its class name and ID, or returns None if not found.
        """
        key = "{}.{}".format(cls, id)
        if key in self.__objects.keys():
            return self.__objects[key]
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage matching a given class name.
        If no class name is provided, counts all objects in storage.
        """
        if cls:
            counter = 0
            for obj in self.__objects.values():
                if obj.__class__.__name__ == cls:
                    counter += 1
            return counter
        return len(self.__objects)

