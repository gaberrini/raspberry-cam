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
