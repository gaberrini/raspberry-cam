import pytest
from flask import Flask
from picamera_server.picamera_server import create_app


@pytest.fixture
def app():
    """
    Flask App factory for running the tests
    :return:
    """
    app = create_app({'TESTING': True})
    yield app


@pytest.fixture
def client(app: Flask):
    """
    Used to make requests to the application when running the tests, without the server running.
    :param app:
    :return:
    """
    return app.test_client()

