import os

# Running settings, options ['development', 'testing']
APP_ENV_TESTING = 'testing'
APP_ENV = os.environ.get('APP_ENV', 'development')

# Server settings
SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = os.environ.get('SERVER_PORT', 8080)
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))
FLASK_INSTANCE_FOLDER = os.path.dirname(__file__)
STATIC_FILES_PATH = os.path.join(FLASK_INSTANCE_FOLDER, 'static')

# Camera settings
DEFAULT_CAPTURE_INTERVAL = os.environ.get('DEFAULT_CAPTURE_INTERVAL', 60)
MIN_CAPTURE_INTERVAL = 2
MAX_CAPTURE_INTERVAL = 600
