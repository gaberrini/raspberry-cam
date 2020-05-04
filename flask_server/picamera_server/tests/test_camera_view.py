"""
Test camera view
"""
from unittest.mock import patch, MagicMock
from jinja2 import TemplateNotFound
from flask import render_template, abort
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.camera_view import ENDPOINTS, TEMPLATES, UI_CAMERA_STREAM, VIDEO_FRAME


class TestCameraView(BaseTestClass):

    @patch('picamera_server.views.camera_view.render_template')
    def test_get_stream(self, mock_render_template: MagicMock):
        """
        Test the UI Stream view

        :param mock_render_template: Magic mock of flask render template
        :return:
        """
        # Mock and data
        mock_render_template.side_effect = render_template
        expected_element = '<img src="{}"'.format(ENDPOINTS[VIDEO_FRAME])

        # When
        response = self.client.get(ENDPOINTS[UI_CAMERA_STREAM])

        # Validation
        self.assertEqual(200, response.status_code)
        self.assertIn(expected_element, str(response.data))
        mock_render_template.assert_called_once_with(TEMPLATES[UI_CAMERA_STREAM], section='stream')

    @patch('picamera_server.views.camera_view.abort')
    @patch('picamera_server.views.camera_view.render_template')
    def test_get_stream_template_not_found(self, mock_render_template: MagicMock, mock_abort: MagicMock):
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
        response = self.client.get(ENDPOINTS[UI_CAMERA_STREAM])

        # Validation
        self.assertEqual(404, response.status_code)
        self.assertIn('404 Not Found', str(response.data))
        mock_abort.assert_called_once_with(404)
