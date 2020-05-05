import os
from typing import Union
from picamera_server.config.logging_config import set_up_logging
from picamera_server.config.database import config_database, get_db_instance
from picamera_server.config.config import FLASK_INSTANCE_FOLDER, APP_ENV_TESTING, APP_ENV_DEVELOPMENT,\
    DevelopmentConfig, TestingConfig
from picamera_server.views.home_view import home
from picamera_server.views.camera_view import camera
from picamera_server.views.capture_mode_view import capture_mode
from picamera_server.views.utils.camera.camera_controllers import init_controllers, set_camera_class
from picamera_server.views.utils.camera.test_camera import TestCamera
from picamera_server.views.utils.camera.pi_camera import PiCamera
from flask import Flask


def create_app(app_env: str = APP_ENV_DEVELOPMENT, test_config: dict = None,
               camera_class: Union[TestCamera, PiCamera, None] = None) -> Flask:
    """
    Initialize the camera controller and
    Configure the Flask app

    :param app_env: App env type
    :param test_config: Dict with config to create the app if its being used for testing
    :param camera_class: Camera class can be specified used for testing
    :return: Flask app
    """
    set_up_logging(app_env)
    config_object_class = DevelopmentConfig

    # Set TestCamera for the camera class when running with test environment
    if app_env == APP_ENV_TESTING:
        set_camera_class(TestCamera)
        config_object_class = TestingConfig

    if camera_class:
        set_camera_class(camera_class)

    init_controllers()

    # Create and configure the app
    app = Flask(__name__, instance_path=FLASK_INSTANCE_FOLDER)
    app.config.from_object(config_object_class())
    if test_config:
        app.config.from_mapping(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(camera)
    app.register_blueprint(capture_mode)

    config_database(app)
    from picamera_server.models.capture import User
    get_db_instance().create_all()

    users  = User.query.all()
    print(users)

    return app
