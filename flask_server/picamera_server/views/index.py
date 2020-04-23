from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound


index_page = Blueprint('index_page', __name__, template_folder='templates')


@index_page.route('/')
def _render():
    try:
        return render_template('base.html')
    except TemplateNotFound:
        abort(404)
