import glob
from typing import List, Optional
from picamera_server import app
from picamera_server.models import CapturedImage
from picamera_server.camera.capture_controller import CaptureController


def create_test_captured_images(number: int = 1, date: Optional[str] = None) -> List[CapturedImage]:
    """
    Create test captured images files and database entries

    :param number: Number of captures to create
    :param date: datetime with DB format to assign to the captures
    :return:
    """
    created = list()
    for i in range(number):
        created.append(CaptureController.create_new_capture(date))

    return created


def captured_images_files() -> List[str]:
    """
    Check the CAPTURES_DIR and all subdirectories and return all the .jpg files found
    :return:
    """
    glob_search_path = '{captures_dir}**/**'.format(captures_dir=app.config["CAPTURES_DIR"])
    return [file for file in glob.glob(glob_search_path, recursive=True) if file.endswith('.jpg')]
