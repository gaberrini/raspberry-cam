from picamera_server.views.utils.camera.camera_controllers import get_capture_controller
from flask import Blueprint, abort, render_template, request, url_for, redirect, current_app
from jinja2 import TemplateNotFound


capture_mode = Blueprint('capture_mode', __name__, template_folder='templates')

FORM_CAPTURE_INTERVAL = 'capture_interval'

UI_CONFIG_CAPTURE_MODE = 'UI_CONFIG_CAPTURE_MODE'
CONFIG_CAPTURE_MODE = 'CONFIG_CAPTURE_MODE'
ENDPOINTS = {
    UI_CONFIG_CAPTURE_MODE: '/camera/ui/capture',
    CONFIG_CAPTURE_MODE: '/camera/config/capture_interval'
}

TEMPLATES = {
    UI_CONFIG_CAPTURE_MODE: 'camera/ui/capture.html'
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
        data = capture_controller.get_interval_values()
        return render_template(TEMPLATES[UI_CONFIG_CAPTURE_MODE], section='capture', data=data)
    except TemplateNotFound:
        abort(404)


@capture_mode.route(ENDPOINTS[CONFIG_CAPTURE_MODE], methods=['POST'])
def config_capture_mode():
    """
    Configure the capture interval value in seconds

    parameters:
        -   name: value
            type: int
            in: query
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
