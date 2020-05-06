import io
import threading
from picamera_server.views.helpers.singleton import Singleton
from picamera_server.camera.base_camera import Camera


PI_CAMERA_IMPORTED = False
try:
    import picamera
    import picamera.exc as picamera_exc
    PI_CAMERA_IMPORTED = True
except ImportError:
    print('Error importing picamera')


class PiCamera(Camera, metaclass=Singleton):
    """
    PiCamera control class, made to control the camera resource, which can be initialized only 1 time.
    If it's initialized multiple times "picamera.PiCamera()" will raise a PiCameraMMALError exception.
    """

    CAPTURE_FORMAT = 'jpeg'

    def __init__(self):
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
            except picamera_exc.PiCameraMMALError as e:
                print('Error enabling camera, looks like it was already enabled. \n {}'.format(e))
                self._close_camera()
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
