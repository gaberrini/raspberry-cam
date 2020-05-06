from picamera_server.camera.camera_controllers import get_camera_controller
from flask import Blueprint, abort, render_template, Response, stream_with_context
from jinja2 import TemplateNotFound


camera = Blueprint('camera', __name__, template_folder='templates')

UI_CAMERA_STREAM = 'UI_CAMERA_STREAM'
VIDEO_FRAME = 'VIDEO_FRAME'
ENDPOINTS = {
    UI_CAMERA_STREAM: '/camera/ui/stream',
    VIDEO_FRAME: '/camera/video_frame',
}

TEMPLATES = {
    UI_CAMERA_STREAM: 'camera/ui/stream.html',
}

MIME_TYPE_MULTIPART_FRAME = 'multipart/x-mixed-replace; boundary=frame'


@camera.route(ENDPOINTS[UI_CAMERA_STREAM], methods=['GET'])
def ui_camera_stream():
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
        return render_template(TEMPLATES[UI_CAMERA_STREAM], section='stream')
    except TemplateNotFound:
        abort(404)


@camera.route(ENDPOINTS[VIDEO_FRAME], methods=['GET'])
def video_frame():
    """
    Endpoint used to feed the video stream with multipart responses

    GET:
    responses:
        200:
            description: multipart/x-mixed-replace; boundary=frame
    :return:
    """
    return Response(stream_with_context(get_camera_controller().frames_generator()),
                    mimetype=MIME_TYPE_MULTIPART_FRAME)
