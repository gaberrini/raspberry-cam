import sys
from picamera_server import app
from picamera_server.config.config import SERVER_HOST, SERVER_PORT


def main():
    """
    Init the Flask App and run the server

    :return:
    """
    debug = False
    if '-debug' in sys.argv:
        debug = True

    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=debug, use_reloader=False)


if __name__ == '__main__':
    main()
