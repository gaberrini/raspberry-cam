import sys
from picamera_server.picamera_server import create_app
from picamera_server.config import SERVER_HOST, SERVER_PORT, APP_ENV


def main():
    """
    Init the Flask App and run the server

    :return:
    """
    debug = False
    if '-debug' in sys.argv:
        debug = True

    app = create_app(app_env=APP_ENV)
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=debug, use_reloader=False)


if __name__ == '__main__':
    main()
