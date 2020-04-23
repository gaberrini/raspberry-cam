import os

SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = os.environ.get('SERVER_PORT', 8080)
SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(16))
FLASK_INSTANCE_FOLDER = os.path.dirname(__file__)
