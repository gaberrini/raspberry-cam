"""
    An emulated camera implementation that streams a repeated sequence of
    files at a rate of one frame per second.
"""
import os
import threading
import time
from typing import List, Optional
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

    def get_frame(self, frame_number: Optional[int] = None, simulate_delay: Optional[bool] = True) -> bytes:
        """
        Return a random test_image
        :param frame_number: optional select specific test frame number
        :param simulate_delay: simulate a delay of 1 second to return the frame
        :return: random test_image
        """
        if simulate_delay:
            time.sleep(1)

        self.lock.acquire()
        frame_number = frame_number if frame_number else int(time.time()) % 3
        _frame = self.frames[frame_number]
        self.lock.release()
        return _frame
