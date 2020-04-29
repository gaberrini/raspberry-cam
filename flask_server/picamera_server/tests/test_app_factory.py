"""
Test the Flask app factory
"""
from picamera_server.picamera_server import create_app


def test_config_by_parameter():
    """
    Test if app apply the test config send by parameter
    :return:
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing
