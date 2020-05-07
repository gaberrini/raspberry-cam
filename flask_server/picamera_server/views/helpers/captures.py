from datetime import datetime
from typing import List
from picamera_server.models import CapturedImage

FRONTEND_TS_FORMAT = '%Y-%m-%dT%H:%M'
DB_TS_FORMAT = '%Y-%m-%d %H:%M:%S.0'
FRONTEND_TS = 'frontend'
DB_TS = 'db'


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


def format_timestamp(timestamp: str,
                     format_origin: str = FRONTEND_TS) -> str:
    """
    Format a str timestamp, from a Frontend format to database format, and backwards

    If the timestamp format is invalid, return empty string

    :param timestamp:
    :param format_origin:
    :return:
    """
    try:
        # From Frontend Format to DB or backwards
        source_format = FRONTEND_TS_FORMAT if format_origin == FRONTEND_TS else DB_TS_FORMAT
        final_format = DB_TS_FORMAT if format_origin == FRONTEND_TS else FRONTEND_TS_FORMAT
        input_date = datetime.strptime(timestamp, source_format)
        formatted_date = input_date.strftime(final_format)
    except ValueError:
        formatted_date = ''

    return formatted_date
