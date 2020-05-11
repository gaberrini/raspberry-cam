import sys
from picamera_server import app
from picamera_server.config.config import SERVER_HOST, SERVER_PORT
from picamera_server.picamera_server import init_camera_controllers


def main():
    """
    Init the Flask App and run the server

    :return:
    """
    debug = False
    if '-debug' in sys.argv:
        debug = True

    init_camera_controllers()
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=debug, use_reloader=False)


if __name__ == '__main__':
    main()
