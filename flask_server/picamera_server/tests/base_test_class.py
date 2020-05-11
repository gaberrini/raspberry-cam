import unittest
import shutil
from picamera_server import app, db
from picamera_server.picamera_server import init_camera_controllers


class BaseTestClass(unittest.TestCase):
    """
    Base class used in test to have in their context:
     - self.app with flask app
     - self.client with the flask test client
     - self.db with the flask db controller

    They are going to be created at the setUp.

    The database will be dropped and created.
    The test tmp CAPTURES_DIR will be clean up
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up for tests
        """
        cls.app = app
        cls.app_context = cls.app.test_request_context()
        cls.app_context.push()
        cls.app_runner = cls.app.test_cli_runner()
        cls.db = db
        cls.client = cls.app.test_client()
        cls.db.drop_all()
        cls.db.create_all()
        init_camera_controllers()
        shutil.rmtree(cls.app.config['CAPTURES_DIR'], ignore_errors=True)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up database
        :return:
        """
        cls.db.drop_all()
        shutil.rmtree(cls.app.config['CAPTURES_DIR'], ignore_errors=True)
