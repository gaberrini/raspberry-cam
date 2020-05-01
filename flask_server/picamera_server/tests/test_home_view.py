"""
Test home view
"""
from unittest.mock import patch, MagicMock
from jinja2 import TemplateNotFound
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.home_view import ENDPOINTS


class TestHomeView(BaseTestClass):

    def test_home_get(self):
        """
        Test the UI Home view
        :return:
        """
        # When
        response = self.client.get(ENDPOINTS['UI_HOME'])

        # Validation
        self.assertEqual(200, response.status_code)
        self.assertIn('Welcome to Raspberry Camera Controller', str(response.data))

    @patch('picamera_server.views.home_view.render_template')
    def test_home_get_template_not_found(self, mock_render_template: MagicMock):
        """
        Test the response when template is not found
        :return:
        """
        # Mock
        mock_render_template.side_effect = TemplateNotFound('template_not_found')

        # When
        response = self.client.get(ENDPOINTS['UI_HOME'])

        # Validation
        self.assertEqual(404, response.status_code)
        self.assertIn('404 Not Found', str(response.data))
