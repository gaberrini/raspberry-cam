import os
from picamera_server.config import FLASK_INSTANCE_FOLDER, SECRET_KEY
from picamera_server.views.home import home
from picamera_server.views.camera import camera
from flask import Flask


def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_path=FLASK_INSTANCE_FOLDER)
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
    )

    os.makedirs(app.instance_path, exist_ok=True)

    # Register Blueprints
    app.register_blueprint(home)
    app.register_blueprint(camera)

    return app
