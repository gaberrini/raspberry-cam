import io
import os
import time
import threading
from typing import Union
from picamera_server.config import STATIC_FILES_PATH, DEFAULT_CAPTURE_INTERVAL, MIN_CAPTURE_INTERVAL,\
    MAX_CAPTURE_INTERVAL
from picamera_server.views.helpers.singleton import Singleton

PI_CAMERA_IMPORTED = False
try:
    import picamera
    from picamera.exc import PiCameraMMALError
    PI_CAMERA_IMPORTED = True
except ImportError:
    print('Error importing picamera')


CAMERA_CONTROLLER = None
CAPTURE_CONTROLLER = None


class TestCamera(object, metaclass=Singleton):
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


class PiCamera(object, metaclass=Singleton):
    """
    PiCamera control class, made to control the camera resource, which can be initialized only 1 time.
    If it's initialized multiple times "picamera.PiCamera()" will raise a PiCameraMMALError exception.
    """

    CAPTURE_FORMAT = 'jpeg'

    def __init__(self):
        print('Initializing camera controller')
        self.camera = picamera.PiCamera()
        self.lock = threading.Lock()

    def _is_camera_enabled(self) -> bool:
        """
        Return if the camera is enabled
        :return: True if camera is enabled, False otherwise
        """
        return not self.camera.closed

    def _enable_camera(self) -> None:
        """
        Enable the camera hardware
        :raises PiCameraMMALError: Exception when camera resources are not free
        :return:
        """
        if not self._is_camera_enabled():
            try:
                self.camera.__init__()
            except PiCameraMMALError as e:
                print('Error enabling camera, looks like it was already enabled. \n {}'.format(e))
                self.camera.close()
                raise e

    def _close_camera(self) -> None:
        """
        Disable the camera
        :return:
        """
        self.camera.close()
        return

    def _get_frame(self, _format: str = 'jpeg') -> bytes:
        """
        Get a frame from the camera and return it, to capture the frame the camera lock will be acquire and release
        when capture finish to avoid exception because resource is already in use
        :param _format: Format of the image, default 'jpeg'. Options: ['jpeg', 'png', 'gif', 'bmp', 'raw', 'bgr, 'bgra']
        :return:
        """
        self.lock.acquire()
        stream = io.BytesIO()
        self.camera.capture(stream, format=_format)
        self.lock.release()
        stream.seek(0)
        return stream.read()

    def get_frame(self) -> bytes:
        """
        Return a frame taken from the camera
        :return:
        """
        self._enable_camera()
        frame = self._get_frame(self.CAPTURE_FORMAT)
        return frame


class CaptureController(object, metaclass=Singleton):
    """
    Class to manage capture mode using the global camera controller.
    Capture mode allows to capture images from the camera with a specific time interval, the interval can go to a
    min value of MIN_CAPTURE_INTERVAL and max value of MAX_CAPTURE_INTERVAL
    """

    CAPTURE_INTERVAL: int = DEFAULT_CAPTURE_INTERVAL
    MAX_CAPTURE_INTERVAL: int = MAX_CAPTURE_INTERVAL
    MIN_CAPTURE_INTERVAL: int = MIN_CAPTURE_INTERVAL

    def __init__(self):
        print('New Camera capture class')
        return

    def _valid_capture_interval(self, capture_interval: Union[str, int]) -> bool:
        """
        Validate if a value is a valid capture interval

        :param capture_interval:
        :return: True if is valid, False otherwise
        """
        return bool(str(capture_interval).isnumeric() and
                    (self.MAX_CAPTURE_INTERVAL >= int(capture_interval) >= self.MIN_CAPTURE_INTERVAL))

    def update_capture_interval(self, capture_interval: Union[str, int]) -> None:
        """
        Update the CAPTURE_INTERVAL value, the function will validate if the value meet the expectations,
        which are:
            - int value
            - bigger than self.MIN_CAPTURE_INTERVAL
            - smaller than self.MAX_CAPTURE_INTERVAL
        :param capture_interval:
        :raises ValueError: if capture interval is invalid
        :return:
        """
        if self._valid_capture_interval(capture_interval):
            self.CAPTURE_INTERVAL = int(capture_interval)
        else:
            raise ValueError('Invalid capture interval value')

    def get_interval_values(self) -> dict:
        """
        Return the values for the interval as a dict.
        Values returned:
            - capture_interval
            - max_interval
            - min_interval

        :return:
        """
        return {'capture_interval': self.CAPTURE_INTERVAL,
                'min_interval': self.MIN_CAPTURE_INTERVAL,
                'max_interval': self.MAX_CAPTURE_INTERVAL}


# Define the Camera class based on the fact if picamera has been imported
Camera = PiCamera if PI_CAMERA_IMPORTED else TestCamera


def init_controllers():
    """
    Init the camera and capture controller. Should be run only once
    :return:
    """
    global CAMERA_CONTROLLER, CAPTURE_CONTROLLER
    print('Starting camera and capture controller')
    CAMERA_CONTROLLER = Camera()
    CAPTURE_CONTROLLER = CaptureController()


def get_camera_controller() -> Camera:
    """
    Return the camera controller.
    :return:
    """
    return CAMERA_CONTROLLER


def get_capture_controller() -> CaptureController:
    """
    Return the capture controller.
    :return:
    """
    return CAPTURE_CONTROLLER
