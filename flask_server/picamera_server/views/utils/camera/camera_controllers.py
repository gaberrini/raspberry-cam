from typing import Union
from picamera_server.views.utils.camera.capture_controller import CaptureController
from picamera_server.views.utils.camera.test_camera import TestCamera
from picamera_server.views.utils.camera.pi_camera import PiCamera, PI_CAMERA_IMPORTED

# Define the Camera class based on the fact if picamera has been imported
CAMERA_CLASS = PiCamera if PI_CAMERA_IMPORTED else TestCamera

CAMERA_CONTROLLER = None
CAPTURE_CONTROLLER = None


def init_controllers():
    """
    Init the camera and capture controller. Should be run only once
    :return:
    """
    global CAMERA_CONTROLLER, CAPTURE_CONTROLLER
    CAMERA_CONTROLLER = CAMERA_CLASS()
    CAPTURE_CONTROLLER = CaptureController()


def set_camera_class(camera_class: Union[type(TestCamera), type(PiCamera)]) -> None:
    """
    Method used to set the global camera class, used in case of testing
    :return:
    """
    global CAMERA_CLASS
    CAMERA_CLASS = camera_class


def get_camera_controller() -> Union[PiCamera, TestCamera]:
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
