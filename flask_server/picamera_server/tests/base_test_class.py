import unittest
from picamera_server import app, db


class BaseTestClass(unittest.TestCase):
    """
    Base class used in test to have in their context:
     - self.app with flask app
     - self.client with the flask test client

    They are going to be created at the setUp
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up for tests
        """
        cls.app = app
        cls.db = db
        cls.client = cls.app.test_client()
        cls.db.drop_all()
        cls.db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up database
        :return:
        """
        cls.db.drop_all()
