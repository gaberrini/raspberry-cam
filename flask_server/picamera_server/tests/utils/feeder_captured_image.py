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
    frame_number = 0
    total_test_frames = len(test_frames)
    for i in range(number):
        test_capture = CapturedImage(image=test_frames[frame_number])
        created_captures.append(test_capture)
        db.session.add(test_capture)
        frame_number += 1
        frame_number = frame_number if total_test_frames > frame_number else 0
    db.session.commit()

    return created_captures
