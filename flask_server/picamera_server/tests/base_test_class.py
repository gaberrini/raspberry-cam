import unittest
from picamera_server import app, db


class BaseTestClass(unittest.TestCase):
    """
    Base class used in test to have in their context:
     - self.app with flask app
     - self.client with the flask test client

    They are going to be created at the setUp
    """

    def setUp(self) -> None:
        """
        Set up for tests
        """
        self.app = app
        self.db = db
        self.client = self.app.test_client()
