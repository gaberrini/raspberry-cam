from picamera_server.views.utils.camera import Camera, get_camera_controller
from flask import Blueprint, abort, render_template, Response
from jinja2 import TemplateNotFound


camera = Blueprint('camera', __name__, template_folder='templates')


@camera.route('/stream')
def stream():
    """
    Path to return the front end for the video stream
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


@camera.route('/video_stream')
def video_stream():
    """
    Endpoint used to feed the video stream with multipart responses
    :return:
    """
    return Response(gen(get_camera_controller()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
