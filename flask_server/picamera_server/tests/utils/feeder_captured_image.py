from typing import List
from picamera_server import db
from picamera_server.models import CapturedImage
from picamera_server.views.utils.camera.test_camera import TestCamera


def create_test_captured_images(number: int = 1) -> List[CapturedImage]:
    """
    Create test captured images and store them in the database

    :param number: Number of captures to create
    :return:
    """
    test_frames = TestCamera().frames
    created_captures = list()
    for i in range(1, number+1):
        test_capture = CapturedImage(image=test_frames[(len(test_frames)-1) % i])
        created_captures.append(test_capture)
        db.session.add(test_capture)
    db.session.commit()

    return created_captures
