from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


camera = Blueprint('camera', __name__, template_folder='templates')


@camera.route('/stream')
def stream():
    try:
        return render_template('camera/stream.html', section='stream')
    except TemplateNotFound:
        abort(404)
