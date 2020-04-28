"""
    An emulated camera implementation that streams a repeated sequence of
    files at a rate of one frame per second.
"""
import os
import threading
import time
from picamera_server.config import STATIC_FILES_PATH
from picamera_server.views.helpers.singleton import Singleton
from picamera_server.views.utils.camera.base_camera import Camera


class TestCamera(Camera, metaclass=Singleton):
    """
        An emulated camera implementation that streams a repeated sequence of
        files [1.jpg, 2.jpg and 3.jpg] at a rate of one frame per second.
    """

    def __init__(self):
        """
        Load the test images to be return when test frames are fetched
        """
        print('Initializing test camera controller')

        test_images_paths = [os.path.join(STATIC_FILES_PATH, 'test_images', number + '.jpg') for number in ['1',
                                                                                                            '2',
                                                                                                            '3']]
        # Cache images to return
        self.frames = [open(file, 'rb').read() for file in test_images_paths]
        # To simulate hardware camera behaviour
        self.lock = threading.Lock()

    def get_frame(self) -> bytes:
        """
        Return a random test_image
        :return: random test_image
        """
        time.sleep(1)
        self.lock.acquire()
        _frame = self.frames[int(time.time()) % 3]
        self.lock.release()
        return _frame
