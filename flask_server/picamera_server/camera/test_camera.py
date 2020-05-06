"""
    An emulated camera implementation that streams a repeated sequence of
    files at a rate of one frame per second.
"""
import os
import threading
import time
from typing import List
from picamera_server.config.config import STATIC_FILES_PATH
from picamera_server.views.helpers.singleton import Singleton
from picamera_server.camera.base_camera import Camera


class TestCamera(Camera, metaclass=Singleton):
    """
        An emulated camera implementation that streams a repeated sequence of
        files [1.jpg, 2.jpg and 3.jpg] at a rate of one frame per second.
    """

    def __init__(self):
        """
        Load the test images to be return when test frames are fetched
        """
        test_images_paths = [os.path.join(STATIC_FILES_PATH, 'test_images', number + '.jpg') for number in ['1',
                                                                                                            '2',
                                                                                                            '3']]

        self.frames = list()
        self._load_test_frames(test_images_paths)

        # To simulate hardware camera behaviour
        self.lock = threading.Lock()

    def _load_test_frames(self, test_images_paths: List[str]) -> None:
        """
        Load the test frames from the files to the instance variable self.frames

        :param test_images_paths: List of paths of images to load in self.frames
        :return:
        """
        # Cache images to return
        for file in test_images_paths:
            with open(file, 'rb') as _file:
                self.frames.append(_file.read())

    def get_frame(self) -> bytes:
        """
        Return a random test_image

        :return: random test_image
        """
        self.lock.acquire()
        _frame = self.frames[int(time.time()) % 3]
        self.lock.release()
        return _frame
