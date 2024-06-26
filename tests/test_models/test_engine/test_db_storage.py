#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

import inspect
import unittest

import pep8

import models
from models.amenity import Amenity
from models.city import City
from models.engine import db_storage
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}

SKIP_DB = models.storage_type != 'db'


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(SKIP_DB, "testing file storage")
    def test_get(self):
        """Test that get method returns the object based on class and id"""
        # Create and save a new object to the database
        new_obj = State(name="Cairo")
        new_obj.save()
        obj_id = new_obj.id
        # Use get method to retrieve the object
        retrieved_obj = models.storage.get(State, obj_id)
        self.assertEqual(retrieved_obj.id, obj_id)
        # Test get method with non-existing id
        self.assertIsNone(models.storage.get(State, "fake-id"))

    @unittest.skipIf(SKIP_DB, "testing file storage")
    def test_count(self):
        """Test that count method returns the correct number of objects"""
        models.storage.reload()
        initial_count = models.storage.count()
        state_count = models.storage.count(State)
        new_obj = State(name="California")
        models.storage.new(new_obj)
        self.assertEqual(models.storage.count(State), state_count + 1)
        self.assertEqual(models.storage.count(), initial_count + 1)
