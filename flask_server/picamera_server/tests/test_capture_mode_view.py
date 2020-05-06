"""
Test camera view
"""
import time
import shutil
from lxml import html
from unittest.mock import patch, MagicMock
from jinja2 import TemplateNotFound
from flask import render_template, abort, redirect
from picamera_server.models import CapturedImage
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.capture_mode_view import ENDPOINTS, TEMPLATES, UI_CONFIG_CAPTURE_MODE,\
    SET_CAPT_INTERVAL_VALUE, FORM_STATUS, SET_STATUS_CAPTURE_MODE, FORM_CAPTURE_INTERVAL, REMOVE_ALL_CAPTURES,\
    UI_CAPTURES_PAGINATED_DEFAULT
from picamera_server.camera.capture_controller import get_capture_controller
from picamera_server.camera.camera_controllers import get_camera_controller
from picamera_server.camera.test_camera import TestCamera
from picamera_server.tests.helpers.captured_image import create_test_captured_images, captured_images_files


class TestCaptureModeView(BaseTestClass):

    def setUp(self) -> None:
        self.db.create_all()
        shutil.rmtree(self.app.config['CAPTURES_DIR'], ignore_errors=True)

    def tearDown(self) -> None:
        self.db.drop_all()
        shutil.rmtree(self.app.config['CAPTURES_DIR'], ignore_errors=True)

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
        expected_data = capture_controller.get_capture_controller_status()
        expected_section = 'capture config'
        expected_edit_interval_form_xpath = '//form[@action="{}" and' \
                                            ' @method="post"]'.format(ENDPOINTS[SET_CAPT_INTERVAL_VALUE])
        expected_delete_form_xpath = '//form[@action="{}" and @method="post"]'.format(ENDPOINTS[REMOVE_ALL_CAPTURES])
        expected_input_xpath = '//input[@min={} and @max={} and' \
                               ' @value={} and @name="{}"]'.format(capture_controller.MIN_CAPTURE_INTERVAL,
                                                                   capture_controller.MAX_CAPTURE_INTERVAL,
                                                                   capture_controller.CAPTURE_INTERVAL,
                                                                   FORM_CAPTURE_INTERVAL)
        expected_input_status_xpath = '//input[@name="{}" and @value="true"]'.format(FORM_STATUS)
        expected_all_captures_button_xpath = '//a[@href="{}"]'.format(ENDPOINTS[UI_CAPTURES_PAGINATED_DEFAULT])

        # When
        response = self.client.get(ENDPOINTS[UI_CONFIG_CAPTURE_MODE])

        # Validation
        html_parser = html.fromstring(str(response.data))
        form_element = html_parser.xpath(expected_edit_interval_form_xpath)
        input_element = html_parser.xpath(expected_input_xpath)

        self.assertEqual(200, response.status_code)
        self.assertTrue(html_parser.xpath(expected_input_status_xpath), 'Input for capture mode status not found')
        self.assertTrue(html_parser.xpath(expected_delete_form_xpath), 'Input for remove captures not found')
        self.assertTrue(html_parser.xpath(expected_all_captures_button_xpath), 'Button to see all captures not found')
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
        response = self.client.post(ENDPOINTS[SET_CAPT_INTERVAL_VALUE])

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
        response = self.client.post(ENDPOINTS[SET_CAPT_INTERVAL_VALUE], data=data)

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
        response = self.client.post(ENDPOINTS[SET_CAPT_INTERVAL_VALUE], data=data)

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
        response = self.client.post(ENDPOINTS[SET_CAPT_INTERVAL_VALUE])

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
        response = self.client.post(ENDPOINTS[SET_CAPT_INTERVAL_VALUE], data=data)

        # Validation
        html_tree = html.fromstring(str(response.data))
        self.assertTrue(html_tree.xpath(expected_element), 'Redirect not found')
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

    @patch('picamera_server.camera.capture_controller.time')
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
            captures_files = captured_images_files()
            self.assertEqual(len(captures), expected_images)
            self.assertEqual(len(captures_files), expected_images)

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

    @patch('picamera_server.views.capture_mode_view.redirect')
    def test_post_remove_all_captures(self, redirect_mock: MagicMock):
        """
        Test post to remove all the stored captures

        :param redirect_mock: MagicMock of flask redirect
        :return:
        """
        # Mock and data
        redirect_mock.side_effect = redirect
        expected_element = '//a[@href="{}"]'.format(ENDPOINTS[UI_CONFIG_CAPTURE_MODE])
        create_test_captured_images(5)

        # When
        response = self.client.post(ENDPOINTS[REMOVE_ALL_CAPTURES])

        # Validation
        html_tree = html.fromstring(str(response.data))
        self.assertTrue(html_tree.xpath(expected_element), 'Redirect not found')
        self.assertEqual(302, response.status_code)
        self.assertEqual(get_capture_controller().get_total_captures(), 0)
        self.assertEqual(len(captured_images_files()), 0)

    @patch('picamera_server.views.capture_mode_view.get_capture_controller')
    @patch('picamera_server.views.capture_mode_view.abort')
    def test_post_remove_all_captures_exception(self, mock_abort: MagicMock, mock_get_capture_controller: MagicMock):
        """
        Test post to remove all the stored captures and there is an exception

        :param mock_abort: MagicMock of flask abort
        :param mock_get_capture_controller: Magic mock of get_capture_controller
        :return:
        """
        # Mock
        # Mock
        mock_abort.side_effect = abort
        mock_capture_controller = MagicMock()
        mock_capture_controller.remove_all_captures.side_effect = Exception('Test')
        mock_get_capture_controller.return_value = mock_capture_controller

        # When
        response = self.client.post(ENDPOINTS[REMOVE_ALL_CAPTURES])

        # Validation
        self.assertEqual(500, response.status_code)
        self.assertIn('Unexpected error', str(response.data))
        mock_abort.assert_called_once_with(500, 'Unexpected error')
