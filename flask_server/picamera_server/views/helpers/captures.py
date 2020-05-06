import base64
from typing import List
from picamera_server.models import CapturedImage


def get_captures_grids(captures: List[CapturedImage], grid_size: int = 4) -> List[object]:
    """
    Return a list of captures grid to send to the templating for showing the captures
    in the UI_CAPTURES_PAGINATED page.

    The images are going to be converted to base64 and decoded to utf-8 to remove the python b' when showing
    bytes, this way we can show the images in the frontend directly

    The grid item will be a dict with the "image" and the "date" of the capture
    :param captures:
    :param grid_size: Number of captures per grid
    :return:
    """
    grids = list()
    new_grid = list()
    for capture in captures:
        if len(new_grid) >= grid_size:
            grids.append(new_grid)
            new_grid = list()

        image = base64.b64encode(capture.image).decode('utf-8')
        new_grid.append({'image': image, 'date': capture.created_at})
    grids.append(new_grid)
    return grids
