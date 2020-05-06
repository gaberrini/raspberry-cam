import base64
from picamera_server.models import CapturedImage
from picamera_server.views.utils.camera.capture_controller import get_capture_controller
from picamera_server.views.helpers.captures import get_captures_grids
from flask import Blueprint, abort, render_template, request, url_for, redirect, current_app
from jinja2 import TemplateNotFound


capture_mode = Blueprint('capture_mode', __name__, template_folder='templates')

FORM_CAPTURE_INTERVAL = 'capture_interval'
FORM_STATUS = 'status'

UI_CONFIG_CAPTURE_MODE = 'UI_CONFIG_CAPTURE_MODE'
UI_CAPTURES_PAGINATED_DEFAULT = 'UI_CAPTURES_PAGINATED_DEFAULT'
UI_CAPTURES_PAGINATED = 'UI_CAPTURES_PAGINATED'
SET_STATUS_CAPTURE_MODE = 'SET_STATUS_CAPTURE_MODE'
SET_CAPT_INTERVAL_VALUE = 'SET_CAPT_INTERVAL_VALUE'
REMOVE_ALL_CAPTURES = 'REMOVE_ALL_CAPTURES'
ENDPOINTS = {
    UI_CONFIG_CAPTURE_MODE: '/camera/ui/captures/config',
    UI_CAPTURES_PAGINATED_DEFAULT: '/camera/ui/captures/',
    UI_CAPTURES_PAGINATED: '/camera/ui/captures/<page_number>',
    SET_CAPT_INTERVAL_VALUE: '/camera/captures/config/capture_interval',
    SET_STATUS_CAPTURE_MODE: '/camera/captures/config/set_status_capture_mode',
    REMOVE_ALL_CAPTURES: '/camera/captures/remove'
}

TEMPLATES = {
    UI_CONFIG_CAPTURE_MODE: 'camera/ui/captures.html',
    UI_CAPTURES_PAGINATED: 'camera/ui/captures/ui_paginated_captures.html'
}


@capture_mode.route(ENDPOINTS[UI_CONFIG_CAPTURE_MODE], methods=['GET'])
def ui_config_capture_mode():
    """
    GET
    responses:
        200:
            description: GUI to manage capture mode
        404:
            description: Template not found
    :return:
    """
    try:
        capture_controller = get_capture_controller()
        data = capture_controller.get_capture_controller_status()
        return render_template(TEMPLATES[UI_CONFIG_CAPTURE_MODE], section='capture config', data=data)
    except TemplateNotFound:
        abort(404)


@capture_mode.route(ENDPOINTS[SET_CAPT_INTERVAL_VALUE], methods=['POST'])
def set_capt_interval_value():
    """
    Configure the capture interval value in seconds

    parameters:
        -   name: value
            type: int
            in: form
            required: true
            description: Value to set the capture interval
    responses:
        200:
            description: Value modified
        400:
            description: Invalid request, value not correct
        500:
            description: Unexpected Error

    :return:
    """
    capture_controller = get_capture_controller()
    capture_interval = request.form.get(FORM_CAPTURE_INTERVAL, '')
    try:
        capture_controller.update_capture_interval(capture_interval)
    except ValueError:
        error_message = 'Form argument {} is required and must be an integer between {} and {}.' \
                        ' Value received: {}'.format(FORM_CAPTURE_INTERVAL,
                                                     capture_controller.MIN_CAPTURE_INTERVAL,
                                                     capture_controller.MAX_CAPTURE_INTERVAL,
                                                     capture_interval)
        current_app.logger.exception(error_message)
        abort(400, error_message)
    except Exception as e:
        current_app.logger.exception('Unexpected exception {}'.format(e))
        abort(500, 'Unexpected error')

    return redirect(url_for('capture_mode.ui_config_capture_mode'))


@capture_mode.route(ENDPOINTS[SET_STATUS_CAPTURE_MODE], methods=['POST'])
def set_status_capture_mode():
    """
    Set the status of the capture mode,
    When the status goes from False to True it will start the capture thread

    parameters:
        -   name: status
            type: bool
            in: form
            required: true
            description: Set capture mode to on / off
    responses:
        200:
            description: Status to set
        500:
            description: Unexpected Error

    :return:
    """
    capture_controller = get_capture_controller()
    status = request.form.get(FORM_STATUS, '')

    if not status:
        abort(400, 'Form argument {} is required must be "True" or "False"'.format(FORM_STATUS))

    try:
        capture_controller.update_capturing_status(status)
    except Exception as e:
        current_app.logger.exception('Unexpected exception {}'.format(e))
        abort(500, 'Unexpected error')

    return redirect(url_for('capture_mode.ui_config_capture_mode'))


@capture_mode.route(ENDPOINTS[REMOVE_ALL_CAPTURES], methods=['POST'])
def remove_all_captures():
    """
    Remove all the stored captures
    responses:
        200:
            description: All captures removed
        500:
            description: Unexpected Error

    :return:
    """
    capture_controller = get_capture_controller()

    try:
        capture_controller.remove_all_captures()
    except Exception as e:
        current_app.logger.exception('Unexpected exception {}'.format(e))
        abort(500, 'Unexpected error')

    return redirect(url_for('capture_mode.ui_config_capture_mode'))


@capture_mode.route(ENDPOINTS[UI_CAPTURES_PAGINATED_DEFAULT], methods=['GET'])
@capture_mode.route(ENDPOINTS[UI_CAPTURES_PAGINATED], methods=['GET'])
def ui_captures_paginated(page_number: int = 1):
    """
    Show the captures paginated

    :param page_number:
    :return:
    """
    items_per_page = current_app.config['ITEMS_PER_PAGE']
    db_captures = CapturedImage.query.paginate(int(page_number), items_per_page, False)
    template_captures_grids = get_captures_grids(db_captures.items)

    template_data = {
        'captures_grids': template_captures_grids,
        'total_captures': db_captures.total,
        'current_page': db_captures.page,
        'next_page': db_captures.next_num,
        'prev_page': db_captures.prev_num
    }

    return render_template(TEMPLATES[UI_CAPTURES_PAGINATED], data=template_data, section='captures')
