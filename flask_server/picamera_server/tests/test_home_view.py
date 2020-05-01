"""
Test home view
"""
from unittest.mock import patch, MagicMock
from jinja2 import TemplateNotFound
from flask import render_template, abort
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.home_view import ENDPOINTS, TEMPLATES


class TestHomeView(BaseTestClass):

    @patch('picamera_server.views.home_view.render_template')
    def test_home_get(self, mock_render_template: MagicMock):
        """
        Test the UI Home view

        :param mock_render_template: Magic mock of flask render template
        :return:
        """
        # Mock
        mock_render_template.side_effect = render_template

        # When
        response = self.client.get(ENDPOINTS['UI_HOME'])

        # Validation
        self.assertEqual(200, response.status_code)
        self.assertIn('Welcome to Raspberry Camera Controller', str(response.data))
        mock_render_template.assert_called_once_with(TEMPLATES['UI_HOME'], section='home')

    @patch('picamera_server.views.home_view.abort')
    @patch('picamera_server.views.home_view.render_template')
    def test_home_get_template_not_found(self, mock_render_template: MagicMock, mock_abort: MagicMock):
        """
        Test the response when template is not found
        Validate abort call

        :param mock_render_template: Magic mock of flask render template
        :param mock_abort: MagicMock of flask abort
        :return:
        """
        # Mock
        mock_render_template.side_effect = TemplateNotFound('template_not_found')
        mock_abort.side_effect = abort

        # When
        response = self.client.get(ENDPOINTS['UI_HOME'])

        # Validation
        self.assertEqual(404, response.status_code)
        self.assertIn('404 Not Found', str(response.data))
        mock_abort.assert_called_once_with(404)
