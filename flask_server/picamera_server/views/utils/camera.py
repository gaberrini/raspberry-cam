import io
import os
import time
from picamera_server.views.utils.singleton import Singleton
from picamera_server.config import STATIC_FILES_PATH
PI_CAMERA_IMPORTED = False
try:
    import picamera
    PI_CAMERA_IMPORTED = True
except ImportError:
    print('Error importing picamera')
    pass


class TestCamera(object, metaclass=Singleton):
    """
        An emulated camera implementation that streams a repeated sequence of
        files [1.jpg, 2.jpg and 3.jpg] at a rate of one frame per second.
    """

    def __init__(self):
        test_images_paths = [os.path.join(STATIC_FILES_PATH, 'test_images', number + '.jpg') for number in ['1',
                                                                                                            '2',
                                                                                                            '3']]
        # Cache images to return
        self.frames = [open(file, 'rb').read() for file in test_images_paths]

    def get_frame(self) -> bytes:
        """
        Return a random test_image
        :return: random test_image
        """
        time.sleep(1)
        return self.frames[int(time.time()) % 3]


class PiCamera(object):

    @staticmethod
    def get_frame() -> bytes:
        """
        Return the current frame from the picamera
        :return:
        """
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()


Camera = PiCamera if PI_CAMERA_IMPORTED else TestCamera
