from typing import Iterator


class Camera(object):
    """
    Camera class that represent needed methods to be used as a camera source for the
    web server
    """

    def get_frame(self) -> bytes:
        """
        Return capture from the camera as an image as bytes
        :return:
        """
        return b''

    def frames_generator(self) -> Iterator[bytes]:
        """
        Generator used to create the multipart responses of frames

        :return: --frame (image/jpeg) part of a multipart response
        """
        while True:
            _frame = self.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n'
                   + _frame + b'\r\n')
