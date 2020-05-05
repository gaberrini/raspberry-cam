import unittest
from picamera_server.picamera_server import create_app
from picamera_server.config.config import APP_ENV_TESTING


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
        self.app = create_app(app_env=APP_ENV_TESTING)
        self.client = self.app.test_client()
