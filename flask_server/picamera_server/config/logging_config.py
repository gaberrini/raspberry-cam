import os
from logging import DEBUG
from logging.config import dictConfig
from picamera_server.config.config import FLASK_INSTANCE_FOLDER, APP_ENV_TESTING, APP_ENV_DEVELOPMENT


LOGGING_FILE_PATH = os.path.join(FLASK_INSTANCE_FOLDER, 'logs', 'logfile.log')
LOGGING_FORMATTER = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'default': {
            'format': LOGGING_FORMATTER,
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file-handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': LOGGING_FILE_PATH,
            'maxBytes': 10*1024*1024,
            'backupCount': 50,
            'level': DEBUG
        }
    },
    'root': {
        'level': DEBUG,
        'handlers': ['console', 'file-handler']
    }
}


def set_up_logging(app_env: str = APP_ENV_DEVELOPMENT) -> None:
    """
    Set up logging using dictConfig

    :param app_env: App env type
    :return:
    """
    os.makedirs(os.path.dirname(LOGGING_FILE_PATH), exist_ok=True)

    logging_conf_dict = LOGGING_CONF.copy()

    # Disable file logging when testing
    if app_env == APP_ENV_TESTING:
        logging_conf_dict['root']['handlers'] = ['console']

    dictConfig(logging_conf_dict)
