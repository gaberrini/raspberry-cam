from picamera_server.views.utils.camera.base_camera import Camera
from picamera_server.views.utils.camera.capture_controller import CaptureController
from picamera_server.views.utils.camera.test_camera import TestCamera
from picamera_server.views.utils.camera.pi_camera import PiCamera, PI_CAMERA_IMPORTED

# Define the Camera class based on the fact if picamera has been imported
CAMERA = PiCamera if PI_CAMERA_IMPORTED else TestCamera

CAMERA_CONTROLLER = None
CAPTURE_CONTROLLER = None


def init_controllers():
    """
    Init the camera and capture controller. Should be run only once
    :return:
    """
    global CAMERA_CONTROLLER, CAPTURE_CONTROLLER
    print('Starting camera and capture controller')
    CAMERA_CONTROLLER = CAMERA()
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
