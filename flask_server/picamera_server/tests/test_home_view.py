"""
Test home view
"""
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.home import ENDPOINTS


class TestHomeView(BaseTestClass):

    def test_home_get(self):
        """
        Test the UI Home view
        :return:
        """
        response = self.client.get(ENDPOINTS['UI_HOME'])
        self.assertEqual(200, response.status_code)
        self.assertIn('Welcome to Raspberry Camera Controller', str(response.data))
