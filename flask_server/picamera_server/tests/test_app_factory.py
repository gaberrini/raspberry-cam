"""
Test the Flask app factory
"""
import unittest
from picamera_server.config.config import APP_ENV_TESTING, APP_ENV_DEVELOPMENT
from picamera_server.picamera_server import create_app


class TestAppFactory(unittest.TestCase):

    def test_config_files_by_app_env(self):
        """
        Test if app apply the config depending on the APP_ENV variable
        :return:
        """
        # Apps creation
        dev_app = create_app()
        test_app = create_app(app_env=APP_ENV_TESTING)

        # Validation
        self.assertEqual(dev_app.env, APP_ENV_DEVELOPMENT)
        self.assertEqual(test_app.env, APP_ENV_TESTING)
