#!/usr/bin/python3
"""
This script encapsulates the DBStorage class for database interactions.
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Dictionary mapping class names to their corresponding classes
class_map = {"Amenity": Amenity, "City": City,
             "Place": Place, "Review": Review, "State": State, "User": User}

class DBStorage:
    """
    This class facilitates interactions with the MySQL database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Constructs a DBStorage object, initializing the database connection.
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Queries the current database session for all objects of a given class.
        """
        new_dict = {}
        for clss in class_map:
            if cls is None or cls is class_map[clss] or cls is clss:
                objs = self.__session.query(class_map[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """
        Adds an object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the current database session if it is not None.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """
        Reloads data from the database, resetting the session.
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """
        Removes the session from the current database session.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieves an object based on its class name and ID, or returns None if not found.
        """
        objects = self.__session.query(class_map[cls])
        for obj in objects:
            if obj.id == id:
                return obj
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage matching a given class name.
        If no class name is provided, counts all objects in storage.
        """
        nobjects = 0
        for clss in class_map:
            if cls is None or cls is class_map[clss] or cls is clss:
                nobjects += len(self.__session.query(class_map[clss]).all())
        return nobjects


