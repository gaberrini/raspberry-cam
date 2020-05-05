"""
Test camera view
"""
import time
from lxml import html
from unittest.mock import patch, MagicMock
from jinja2 import TemplateNotFound
from flask import render_template, abort, redirect
from picamera_server.models import CapturedImage
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.capture_mode_view import ENDPOINTS, TEMPLATES, UI_CONFIG_CAPTURE_MODE, CONFIG_CAPTURE_MODE, \
    FORM_CAPTURE_INTERVAL, FORM_STATUS, SET_STATUS_CAPTURE_MODE
from picamera_server.views.utils.camera.capture_controller import get_capture_controller
from picamera_server.views.utils.camera.camera_controllers import get_camera_controller
from picamera_server.views.utils.camera.test_camera import TestCamera


class TestCaptureModeView(BaseTestClass):

    @patch('picamera_server.views.capture_mode_view.render_template')
    def test_get_ui_config_capture_mode(self, mock_render_template: MagicMock):
        """
        Test the UI of capture mode

        :param mock_render_template: Magic mock of flask render template
        :return:
        """
        # Mock and data
        capture_controller = get_capture_controller()
        mock_render_template.side_effect = render_template
        expected_data = capture_controller.get_interval_values()
        expected_section = 'capture'
        expected_form_xpath = '//form[@action="{}" and @method="post"]'.format(ENDPOINTS[CONFIG_CAPTURE_MODE])
        expected_input_xpath = '//input[@min={} and @max={} and' \
                               ' @value={}]'.format(capture_controller.MIN_CAPTURE_INTERVAL,
                                                    capture_controller.MAX_CAPTURE_INTERVAL,
                                                    capture_controller.CAPTURE_INTERVAL)

        # When
        response = self.client.get(ENDPOINTS[UI_CONFIG_CAPTURE_MODE])

        # Validation
        html_parser = html.fromstring(str(response.data))
        form_element = html_parser.xpath(expected_form_xpath)
        input_element = html_parser.xpath(expected_input_xpath)

        self.assertEqual(200, response.status_code)
        self.assertTrue(form_element, 'Form to update capture interval not found')
        self.assertTrue(input_element, 'Input to show and update capture interval not found')
        mock_render_template.assert_called_once_with(TEMPLATES[UI_CONFIG_CAPTURE_MODE], section=expected_section,
                                                     data=expected_data)

    @patch('picamera_server.views.capture_mode_view.abort')
    @patch('picamera_server.views.capture_mode_view.render_template')
    def test_get_ui_config_capture_mode_not_found(self, mock_render_template: MagicMock, mock_abort: MagicMock):
        """
        Test template not found for ui config capture mode

        :param mock_render_template: Magic mock of flask render template
        :param mock_abort: MagicMock of flask abort
        :return:
        """
        # Mock
        mock_render_template.side_effect = TemplateNotFound('template_not_found')
        mock_abort.side_effect = abort

        # When
        response = self.client.get(ENDPOINTS[UI_CONFIG_CAPTURE_MODE])

        # Validation
        self.assertEqual(404, response.status_code)
        self.assertIn('404 Not Found', str(response.data))
        mock_abort.assert_called_once_with(404)

    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_config_capture_mode_bad_request(self, mock_abort: MagicMock):
        """
        Test post to config the capture interval bad request

        :param mock_abort: MagicMock of flask abort
        :return:
        """
        # Mock
        mock_abort.side_effect = abort

        # When
        response = self.client.post(ENDPOINTS[CONFIG_CAPTURE_MODE])

        # Validation
        self.assertEqual(400, response.status_code)
        self.assertIn('Form argument {}'.format(FORM_CAPTURE_INTERVAL), str(response.data))
        mock_abort.assert_called_once()
        self.assertEqual(mock_abort.call_args[0][0], 400)

    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_config_capture_mode_bad_request_small_value(self, mock_abort: MagicMock):
        """
        Test post to config the capture interval bad request small value

        :param mock_abort: MagicMock of flask abort
        :return:
        """
        # Mock
        mock_abort.side_effect = abort
        data = {FORM_CAPTURE_INTERVAL: get_capture_controller().MIN_CAPTURE_INTERVAL - 1}

        # When
        response = self.client.post(ENDPOINTS[CONFIG_CAPTURE_MODE], data=data)

        # Validation
        self.assertEqual(400, response.status_code)
        self.assertIn('Form argument {}'.format(FORM_CAPTURE_INTERVAL), str(response.data))
        mock_abort.assert_called_once()
        self.assertEqual(mock_abort.call_args[0][0], 400)

    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_config_capture_mode_bad_request_big_value(self, mock_abort: MagicMock):
        """
        Test post to config the capture interval bad request big value

        :param mock_abort: MagicMock of flask abort
        :return:
        """
        # Mock
        mock_abort.side_effect = abort
        data = {FORM_CAPTURE_INTERVAL: get_capture_controller().MAX_CAPTURE_INTERVAL + 1}

        # When
        response = self.client.post(ENDPOINTS[CONFIG_CAPTURE_MODE], data=data)

        # Validation
        self.assertEqual(400, response.status_code)
        self.assertIn('Form argument {}'.format(FORM_CAPTURE_INTERVAL), str(response.data))
        mock_abort.assert_called_once()
        self.assertEqual(mock_abort.call_args[0][0], 400)

    @patch('picamera_server.views.capture_mode_view.get_capture_controller')
    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_config_capture_mode_exception(self, mock_abort: MagicMock, mock_get_capture_controller: MagicMock):
        """
        Test post to config the capture interval exception

        :param mock_abort: MagicMock of flask abort
        :param mock_get_capture_controller: Magic mock of get_capture_controller
        :return:
        """
        # Mock
        mock_abort.side_effect = abort
        mock_capture_controller = MagicMock()
        mock_capture_controller.update_capture_interval.side_effect = Exception('Test')
        mock_get_capture_controller.return_value = mock_capture_controller

        # When
        response = self.client.post(ENDPOINTS[CONFIG_CAPTURE_MODE])

        # Validation
        self.assertEqual(500, response.status_code)
        self.assertIn('Unexpected error', str(response.data))
        mock_abort.assert_called_once_with(500, 'Unexpected error')

    @patch('picamera_server.views.capture_mode_view.redirect')
    def test_post_config_capture_mode_success(self, redirect_mock: MagicMock):
        """
        Test post to config the capture interval

        :param redirect_mock: MagicMock of flask redirect
        :return:
        """
        # Mock
        redirect_mock.side_effect = redirect
        test_interval = 10
        data = {FORM_CAPTURE_INTERVAL: test_interval}
        expected_element = '//a[@href="{}"]'.format(ENDPOINTS[UI_CONFIG_CAPTURE_MODE])

        # When
        response = self.client.post(ENDPOINTS[CONFIG_CAPTURE_MODE], data=data)

        # Validation
        html_tree = html.fromstring(str(response.data))
        self.assertTrue(html_tree.xpath(expected_element))
        self.assertEqual(302, response.status_code)
        self.assertEqual(get_capture_controller().CAPTURE_INTERVAL, test_interval)

    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_set_status_capture_mode_bad_request(self, mock_abort: MagicMock):
        """
        Test post to set the capture mode status, without sending form argument

        :param mock_abort: MagicMock of flask abort
        :return:
        """
        # Mock
        mock_abort.side_effect = abort

        # When
        response = self.client.post(ENDPOINTS[SET_STATUS_CAPTURE_MODE])

        # Validation
        self.assertEqual(400, response.status_code)
        self.assertIn('Form argument {}'.format(FORM_STATUS), str(response.data))
        mock_abort.assert_called_once()
        self.assertEqual(mock_abort.call_args[0][0], 400)

    @patch('picamera_server.views.utils.camera.capture_controller.time')
    @patch('picamera_server.views.capture_mode_view.redirect')
    def test_post_set_status_capture_mode(self, redirect_mock: MagicMock, time_mock: MagicMock):
        """
        Test post to set the capture mode status and start the capture thread

        :param time_mock: Time.sleep mock to control the capture thread
        :param redirect_mock: MagicMock of flask redirect
        :return:
        """
        # Mock
        # Lets kill the capture thread with an exception
        time_mock.sleep.side_effect = [time.sleep, time.sleep, time.sleep, Exception('Test')]
        redirect_mock.side_effect = redirect
        capture_controller = get_capture_controller()
        expected_images = 4
        capture_interval = 0
        sleep_time = 3
        test_frames = get_camera_controller().frames + [get_camera_controller().frames[0]]
        capture_controller.CAPTURE_INTERVAL = capture_interval

        with patch.object(TestCamera, 'get_frame', side_effect=test_frames) as _:
            # When
            response = self.client.post(ENDPOINTS[SET_STATUS_CAPTURE_MODE], data={FORM_STATUS: 'true'})

            # Validation 1
            self.assertEqual(302, response.status_code)
            self.assertEqual(get_capture_controller().CAPTURING_STATUS, True)
            time.sleep(sleep_time)

            # When 2
            response = self.client.post(ENDPOINTS[SET_STATUS_CAPTURE_MODE], data={FORM_STATUS: 'false'})

            # Validation 2
            self.assertEqual(302, response.status_code)
            self.assertEqual(get_capture_controller().CAPTURING_STATUS, False)
            self.assertEqual(get_capture_controller().CAPTURING_THREAD, None)
            captures = CapturedImage.query.all()
            self.assertEqual(len(captures), expected_images)
            self.assertEqual(captures[0].image, test_frames[0])
            self.assertEqual(captures[1].image, test_frames[1])
            self.assertEqual(captures[2].image, test_frames[2])
            self.assertEqual(captures[3].image, test_frames[0])

    @patch('picamera_server.views.capture_mode_view.get_capture_controller')
    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_set_status_capture_mode_exception(self, mock_abort: MagicMock, mock_get_capture_controller: MagicMock):
        """
        Test post to set the capture interval status, when there is an exception

        :param mock_abort: MagicMock of flask abort
        :param mock_get_capture_controller: Magic mock of get_capture_controller
        :return:
        """
        # Mock
        mock_abort.side_effect = abort
        mock_capture_controller = MagicMock()
        mock_capture_controller.update_capturing_status.side_effect = Exception('Test')
        mock_get_capture_controller.return_value = mock_capture_controller
        data = {FORM_STATUS: 'true'}

        # When
        response = self.client.post(ENDPOINTS[SET_STATUS_CAPTURE_MODE], data=data)

        # Validation
        self.assertEqual(500, response.status_code)
        self.assertIn('Unexpected error', str(response.data))
        mock_abort.assert_called_once_with(500, 'Unexpected error')
