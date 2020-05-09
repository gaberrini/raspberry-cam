from flask import Blueprint, render_template, abort
from flask_login import login_required
from jinja2 import TemplateNotFound


home = Blueprint('home', __name__, template_folder='templates')

UI_HOME = 'UI_HOME'
ENDPOINTS = {
    UI_HOME: '/',
}

TEMPLATES = {
    UI_HOME: 'home.html',
}


@home.route(ENDPOINTS[UI_HOME])
@login_required
def ui_home():
    """
    GET
    responses:
        200:
            description: Home page
        404:
            description: Template not found
    :return:
    """
    try:
        return render_template(TEMPLATES[UI_HOME], section='home')
    except TemplateNotFound:
        abort(404)
