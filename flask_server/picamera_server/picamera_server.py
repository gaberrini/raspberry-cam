import os
from picamera_server.config import FLASK_INSTANCE_FOLDER, SECRET_KEY
from picamera_server.views.home import home
from picamera_server.views.camera import camera
from picamera_server.views.utils.camera.camera import init_controllers
from flask import Flask


def create_app(test_config: dict = None) -> Flask:
    """
    Initialize the camera controller and
    Configure the Flask app

    :param test_config: Dict with config to create the app if its being used for testing
    :return: Flask app
    """
    init_controllers()

    # Create and configure the app
    app = Flask(__name__, instance_path=FLASK_INSTANCE_FOLDER)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
    )

    if test_config:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(camera)

    return app
