import os
from picamera_server.config.logging_config import set_up_logging
from picamera_server.config.config import FLASK_INSTANCE_FOLDER, APP_ENV_TESTING, APP_ENV_DEVELOPMENT,\
    DevelopmentConfig, TestingConfig, APP_ENV
from flask import Flask


def register_blueprints(app: Flask) -> None:
    """
    Register the blueprints to the app
    We make the imports of the blueprints here to avoid pre load of the views when the app and database
     are not yet properly configured

    :param app:
    :return:
    """
    from picamera_server.views.home_view import home
    from picamera_server.views.camera_view import camera
    from picamera_server.views.capture_mode_view import capture_mode

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(camera)
    app.register_blueprint(capture_mode)


def init_camera_controllers() -> None:
    """
    Init the camera and camera capture controllers

    :return:
    """
    from picamera_server.views.utils.camera.camera_controllers import init_camera_controller, set_camera_class
    from picamera_server.views.utils.camera.capture_controller import init_capture_controller
    from picamera_server.views.utils.camera.test_camera import TestCamera

    # Set TestCamera for the camera class when running with test environment
    if APP_ENV == APP_ENV_TESTING:
        set_camera_class(TestCamera)

    init_camera_controller()
    init_capture_controller()


def create_app(app_env: str = APP_ENV_DEVELOPMENT) -> Flask:
    """
    Initialize the camera controller and
    Configure the Flask app

    :param app_env: App env type
    :return: Flask app
    """
    set_up_logging(app_env)
    config_object_class = DevelopmentConfig

    # Set TestCamera for the camera class when running with test environment
    if app_env == APP_ENV_TESTING:
        config_object_class = TestingConfig

    # Create and configure the app
    app = Flask(__name__, instance_path=FLASK_INSTANCE_FOLDER)
    app.config.from_object(config_object_class())

    os.makedirs(app.instance_path, exist_ok=True)

    return app
