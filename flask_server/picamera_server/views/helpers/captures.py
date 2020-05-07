from typing import List
from picamera_server.models import CapturedImage


def get_captures_grids(captures: List[CapturedImage], grid_size: int = 4) -> List[object]:
    """
    Return a list of captures grid to send to the templating for showing the captures
    in the UI_CAPTURES_PAGINATED page.


    The grid item will be a dict with the "image" (relative_path) and the "date" of the capture
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

        new_grid.append({'image': capture.relative_path, 'date': capture.created_at})
    grids.append(new_grid)
    return grids
