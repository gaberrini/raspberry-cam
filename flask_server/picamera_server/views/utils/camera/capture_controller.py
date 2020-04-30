from typing import Union
from picamera_server.config import DEFAULT_CAPTURE_INTERVAL, MIN_CAPTURE_INTERVAL,\
    MAX_CAPTURE_INTERVAL
from picamera_server.views.helpers.singleton import Singleton


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
        print('Init capture controller')

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
