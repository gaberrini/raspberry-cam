import os


# Env options ['development', 'testing', 'production']
APP_ENV_TESTING = 'testing'
APP_ENV_DEVELOPMENT = 'development'
APP_ENV = os.environ.get('APP_ENV', APP_ENV_DEVELOPMENT)

# Server settings
SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = os.environ.get('SERVER_PORT', 8080)

FLASK_INSTANCE_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
STATIC_FILES_PATH = os.path.join(FLASK_INSTANCE_FOLDER, 'static')
DEFAULT_SQL_LITE_DATABASE = 'sqlite:///{}'.format(os.path.join(FLASK_INSTANCE_FOLDER, 'sqlite.db'))
TEST_SQL_LITE_DATABASE = 'sqlite:///{}'.format(os.path.join(FLASK_INSTANCE_FOLDER, 'test_sqlite.db'))

# Camera settings
DEFAULT_CAPTURE_INTERVAL = os.environ.get('DEFAULT_CAPTURE_INTERVAL', 60)
MIN_CAPTURE_INTERVAL = 0
MAX_CAPTURE_INTERVAL = 600


class Config(object):
    """Base config."""
    DEBUG = True
    TESTING = False
    APP_ENV = APP_ENV_DEVELOPMENT
    ENV = APP_ENV_DEVELOPMENT
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', DEFAULT_SQL_LITE_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    APP_ENV = APP_ENV_DEVELOPMENT
    ENV = APP_ENV_DEVELOPMENT


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    ENV = APP_ENV_TESTING
    APP_ENV = APP_ENV_TESTING
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test'
    SQLALCHEMY_DATABASE_URI = TEST_SQL_LITE_DATABASE
