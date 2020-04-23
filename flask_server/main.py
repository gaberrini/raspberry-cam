import sys
from picamera_server.picamera_server import create_app
from picamera_server.config import SERVER_HOST, SERVER_PORT


def main():
    debug = False
    if '-debug' in sys.argv:
        debug = True

    app = create_app()
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=debug)


if __name__ == '__main__':
    main()
