import datetime
import io
import os
import time
from threading import Thread
from typing import Union, Optional
from PIL import Image
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

    @staticmethod
    def _save_capture_to_file(capture: bytes) -> str:
        """
        Save the capture as bytes as a file.
        It will be stored in the CAPTURES_DIR.
        Inside the dir the captures will be split in folders by days.
        The folder naming format will be %y-%m-%d

        :param capture:
        :return: Relative path of the file from the CAPTURES_DIR
        """
        captured_image = Image.open(io.BytesIO(capture))
        current_time = datetime.datetime.now()
        timestamp = current_time.strftime('%y-%m-%d-%H-%M-%S-%f')
        day_folder = '{year}-{month}-{day}'.format(year=current_time.year,
                                                   month=current_time.month,
                                                   day=current_time.day)
        relative_path = os.path.join(day_folder, '{}.jpg'.format(timestamp))
        file_path = os.path.join(app.config['CAPTURES_DIR'], relative_path)

        try:
            captured_image.save(file_path, 'JPEG')
        # If the day folder is not created we create it and save the image
        except FileNotFoundError:
            os.makedirs(os.path.dirname(file_path))
            captured_image.save(file_path, 'JPEG')

        return relative_path

    @staticmethod
    def _new_captured_image_db_entry(relative_path: str) -> CapturedImage:
        """
        Create a new CapturedImage entry in the db

        :param relative_path: Relative path to assign to the new entry
        :return:
        """
        new_capture = CapturedImage(relative_path=relative_path)
        db.session.add(new_capture)
        db.session.commit()
        return new_capture

    @staticmethod
    def _create_new_capture() -> None:
        """
        Take a new capture from the camera controller
        Store it as a file and
        Create the CapturedImage entry in db

        :return:
        """
        camera_controller = get_camera_controller()
        capture_as_bytes = camera_controller.get_frame()

        relative_file_path = CaptureController._save_capture_to_file(capture_as_bytes)
        CaptureController._new_captured_image_db_entry(relative_file_path)

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
            while self.CAPTURING_STATUS:
                self._create_new_capture()
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
