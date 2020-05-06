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

    @staticmethod
    def _get_multipart_frame(frame: bytes):
        """
        Frame returned as a frame of a multipart response

        :param frame:
        :return:
        """
        return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'

    def frames_generator(self) -> Iterator[bytes]:
        """
        Generator used to create the multipart responses of frames

        :return: --frame (image/jpeg) part of a multipart response
        """
        while True:
            frame = self.get_frame()
            yield self._get_multipart_frame(frame)
