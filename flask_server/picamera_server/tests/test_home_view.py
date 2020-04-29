"""
Test home view
"""
from picamera_server.views.home import ENDPOINTS
from flask.testing import FlaskClient


def test_home(client: FlaskClient):
    """
    Test the UI Home view
    :param client:
    :return:
    """
    response = client.get(ENDPOINTS['UI_HOME'])
    assert response.status_code == 200
    assert 'Welcome to Raspberry Camera Controller' in str(response.data)
