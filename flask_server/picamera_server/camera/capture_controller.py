import time
from threading import Thread
from typing import Union, Optional
from picamera_server import db, app
from picamera_server.config.config import DEFAULT_CAPTURE_INTERVAL, MIN_CAPTURE_INTERVAL,\
    MAX_CAPTURE_INTERVAL
from picamera_server.models.captured_image import CapturedImage
from picamera_server.camera.camera_controllers import get_camera_controller
from picamera_server.views.helpers.singleton import Singleton


CAPTURE_CONTROLLER = None


class CaptureController(object, metaclass=Singleton):
    """
    Class to manage capture mode using the global camera controller.
    Capture mode allows to capture images from the camera with a specific time interval, the interval can go to a
    min value of MIN_CAPTURE_INTERVAL and max value of MAX_CAPTURE_INTERVAL
    """

    CAPTURING_THREAD: Optional[Thread] = None
    CAPTURING_STATUS: bool = False
    CAPTURE_INTERVAL: int = DEFAULT_CAPTURE_INTERVAL
    MAX_CAPTURE_INTERVAL: int = MAX_CAPTURE_INTERVAL
    MIN_CAPTURE_INTERVAL: int = MIN_CAPTURE_INTERVAL

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

    def get_capture_controller_status(self) -> dict:
        """
        Return the values for the controller properties.
        Values returned:
            - capture_interval
            - max_interval
            - min_interval
            - capturing_status
            - ui_capture_mode_status used by frontend
            - ui_total_captures number of captures stored

        :return:
        """
        ui_capture_mode_status = 'RUNNING' if self.CAPTURING_STATUS else 'STOPPED'
        return {'capture_interval': self.CAPTURE_INTERVAL,
                'min_interval': self.MIN_CAPTURE_INTERVAL,
                'max_interval': self.MAX_CAPTURE_INTERVAL,
                'capturing_status': self.CAPTURING_STATUS,
                'ui_capture_mode_status': ui_capture_mode_status,
                'ui_total_captures': self.get_total_captures()}

    def update_capturing_status(self, new_status: str):
        """
        Update the CAPTURING_STATUS flag, to validate if the capture_thread should keep storing images or stop.
        When the CAPTURING_STATUS flag is set to True, the capture_thread will be launched if it's not already running

        :param new_status: New capturing status to set because the argument come throw the html form we will receive it
            as string, we will make the new_status to True if new_status.lower() == 'true', otherwise will be False
        :return:
        """
        new_status = new_status.lower() == 'true'
        self.CAPTURING_STATUS = new_status

        if self.CAPTURING_STATUS:
            if not self.CAPTURING_THREAD:
                self.CAPTURING_THREAD = Thread(target=self.capture_thread, daemon=True)
                self.CAPTURING_THREAD.start()

    def capture_thread(self):
        """
        Function that will be used to run the capture thread.
        This function will store the captures every CAPTURE_INTERVAL seconds

        :return:
        """
        try:
            camera_controller = get_camera_controller()

            while self.CAPTURING_STATUS:
                capture = camera_controller.get_frame()
                new_capture = CapturedImage(image=capture)
                db.session.add(new_capture)
                db.session.commit()
                # Todo: when the thread is sleep and we start the interval again or reduce the interval, it still
                # Todo: need to wait for this sleep to finish, this needs to be improved
                time.sleep(self.CAPTURE_INTERVAL)
        except Exception as e:
            app.logger.exception('Exception in capture thread {}'.format(e))
        finally:
            self.CAPTURING_THREAD = None

    @staticmethod
    def get_total_captures() -> int:
        """
        Return the total number of stored captures
        :return:
        """
        return CapturedImage.query.count()

    @staticmethod
    def remove_all_captures() -> int:
        """
        Remove all the stored captures
        :return: Number of deleted rows
        """
        deleted = CapturedImage.query.delete()
        db.session.commit()
        return deleted


def init_capture_controller():
    """
    Init capture controller. Should be run only once
    :return:
    """
    global CAPTURE_CONTROLLER
    CAPTURE_CONTROLLER = CaptureController()


def get_capture_controller() -> Optional[CaptureController]:
    """
    Return the capture controller.
    :return:
    """
    return CAPTURE_CONTROLLER
