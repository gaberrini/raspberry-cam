from picamera_server.views.utils.camera import Camera, get_camera_controller, get_capture_controller
from flask import Blueprint, abort, render_template, Response, request, jsonify
from jinja2 import TemplateNotFound


camera = Blueprint('camera', __name__, template_folder='templates')


@camera.route('/camera/ui/stream', methods=['GET'])
def stream():
    """
    GET return the GUI for the video stream
    :return:
    """
    try:
        return render_template('camera/stream.html', section='stream')
    except TemplateNotFound:
        abort(404)


def gen(_camera: Camera) -> bytes:
    """
    Generator used to create the multipart responses
    :param _camera:
    :return: --frame (image/jpeg) part of a multipart responses
    """
    while True:
        _frame = _camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + _frame + b'\r\n')


@camera.route('/camera/video_stream', methods=['GET'])
def video_stream():
    """
    Endpoint used to feed the video stream with multipart responses
    :return:
    """
    return Response(gen(get_camera_controller()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@camera.route('/camera/ui/capture', methods=['GET'])
def capture():
    """
    GET Return the GUI to manage the capture mode
    :return:
    """
    try:
        capture_controller = get_capture_controller()
        data = {
            'capture_interval': capture_controller.CAPTURE_INTERVAL,
            'min_interval': capture_controller.MIN_CAPTURE_INTERVAL,
            'max_interval': capture_controller.MAX_CAPTURE_INTERVAL
        }
        return render_template('camera/capture.html', section='capture', data=data)
    except TemplateNotFound:
        abort(404)


@camera.route('/camera/config/capture_interval', methods=['POST'])
def config_capture_interval():
    """
    Configure the capture interval value expects JSON

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

    :return:
    """
    capture_controller = get_capture_controller()
    capture_interval = request.args.get('capture_interval', '')

    try:
        capture_controller.update_capture_interval(capture_interval)
    except ValueError:
        abort(400, 'Query argument capture_interval is required and must be an integer between {} and {}.'
                   ' Value received: {}'
              .format(capture_controller.MIN_CAPTURE_INTERVAL, capture_controller.MAX_CAPTURE_INTERVAL,
                      capture_interval))

    return jsonify({'capture_interval': capture_interval})
