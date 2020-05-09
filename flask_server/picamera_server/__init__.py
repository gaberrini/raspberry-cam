from flask_login import LoginManager
from picamera_server.picamera_server import create_app, register_blueprints, init_camera_controllers
from picamera_server.config.database import config_database
from picamera_server.config.config import APP_ENV
from picamera_server.config.login_manager import init_login_manager

app = create_app(app_env=APP_ENV)
db = config_database(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Load later due to dependencies of config_database
import picamera_server.models

db.create_all()

init_camera_controllers()
register_blueprints(app)
login_manager = init_login_manager(login_manager)
