from picamera_server.views.utils.camera.base_camera import Camera
from picamera_server.views.utils.camera.camera import get_camera_controller, get_capture_controller
from flask import Blueprint, abort, render_template, Response, request, url_for, redirect
from jinja2 import TemplateNotFound


camera = Blueprint('camera', __name__, template_folder='templates')

ENDPOINTS = {
    'UI_CAMERA_STREAM': '/camera/ui/stream',
    'UI_CONFIG_CAPTURE_MODE': '/camera/ui/capture',
    'VIDEO_FRAME': '/camera/video_stream',
    'CONFIG_CAPTURE_MODE': '/camera/config/capture_interval'
}


@camera.route(ENDPOINTS['UI_CAMERA_STREAM'], methods=['GET'])
def stream():
    """
    GET
    responses:
        200:
            description: GUI for the video stream
        404:
            description: Template not found
    :return:
    """
    try:
        return render_template('camera/stream.html', section='stream')
    except TemplateNotFound:
        abort(404)


def gen(_camera: Camera) -> bytes:
    """
    Generator used to create the multipart responses

    :param _camera: Camera with method get_frame
    :return: --frame (image/jpeg) part of a multipart response
    """
    while True:
        _frame = _camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + _frame + b'\r\n')


@camera.route(ENDPOINTS['VIDEO_FRAME'], methods=['GET'])
def video_stream():
    """
    Endpoint used to feed the video stream with multipart responses

    GET:
    responses:
        200:
            description: multipart/x-mixed-replace; boundary=frame
    :return:
    """
    return Response(gen(get_camera_controller()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@camera.route(ENDPOINTS['UI_CONFIG_CAPTURE_MODE'], methods=['GET'])
def capture():
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
        return render_template('camera/capture.html', section='capture', data=data)
    except TemplateNotFound:
        abort(404)


@camera.route(ENDPOINTS['CONFIG_CAPTURE_MODE'], methods=['POST'])
def config_capture_interval():
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
    capture_interval = request.form.get('capture_interval', '')
    try:
        capture_controller.update_capture_interval(capture_interval)
    except ValueError:
        abort(400, 'Query argument capture_interval is required and must be an integer between {} and {}.'
                   ' Value received: {}'
              .format(capture_controller.MIN_CAPTURE_INTERVAL, capture_controller.MAX_CAPTURE_INTERVAL,
                      capture_interval))
    except Exception as e:
        print('Unexpected exception {}'.format(e))
        abort(500, 'Unexpected error')

    return redirect(url_for('camera.capture'))
