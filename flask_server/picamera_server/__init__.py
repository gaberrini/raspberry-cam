from picamera_server.picamera_server import create_app, register_blueprints, init_camera_controllers
from picamera_server.config.database import config_database
from picamera_server.config.config import APP_ENV

app = create_app(app_env=APP_ENV)
db = config_database(app)

import picamera_server.models

db.create_all()

init_camera_controllers()
register_blueprints(app)
