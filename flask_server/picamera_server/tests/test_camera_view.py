"""
Test camera view
"""
from lxml import html
from unittest.mock import patch, MagicMock
from jinja2 import TemplateNotFound
from flask import render_template, abort, Response
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.camera.base_camera import Camera
from picamera_server.camera.test_camera import TestCamera
from picamera_server.views.camera_view import ENDPOINTS, TEMPLATES, UI_CAMERA_STREAM, VIDEO_FRAME,\
    MIME_TYPE_MULTIPART_FRAME, get_camera_controller


class TestCameraView(BaseTestClass):

    @patch('picamera_server.views.camera_view.render_template')
    def test_get_ui_camera_stream(self, mock_render_template: MagicMock):
        """
        Test the UI Stream view

        :param mock_render_template: Magic mock of flask render template
        :return:
        """
        # Mock and data
        mock_render_template.side_effect = render_template
        img_source_element_xpath = '//img[@src="{}"]'.format(ENDPOINTS[VIDEO_FRAME])

        # When
        response = self.client.get(ENDPOINTS[UI_CAMERA_STREAM])

        # Validation
        html_tree = html.fromstring(str(response.data))

        self.assertEqual(200, response.status_code)
        self.assertTrue(html_tree.xpath(img_source_element_xpath), 'Img element to stream not found')
        mock_render_template.assert_called_once_with(TEMPLATES[UI_CAMERA_STREAM], section='stream')

    @patch('picamera_server.views.camera_view.abort')
    @patch('picamera_server.views.camera_view.render_template')
    def test_get_ui_camera_stream_template_not_found(self, mock_render_template: MagicMock, mock_abort: MagicMock):
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

    @patch('picamera_server.views.camera_view.stream_with_context')
    @patch('picamera_server.views.camera_view.Response')
    def test_get_video_frame_test_camera_1(self, mock_response: MagicMock, mock_stream_with_context: MagicMock):
        """
        Test the Video stream endpoint,
        Create a list of expected frames and then StopIteration

        :param mock_response: Magic mock of flask Response
        :param mock_stream_with_context: Magic mock of flask stream_with_context
        :return:
        """
        # Mock and data
        test_generator = get_camera_controller().frames_generator()
        test_frames = get_camera_controller().frames

        mock_stream_with_context.return_value = test_generator
        mock_response.side_effect = Response

        expected_multipart_frames = [Camera._get_multipart_frame(test_frames[0]),
                                     Camera._get_multipart_frame(test_frames[1]),
                                     Camera._get_multipart_frame(test_frames[2])]

        with patch.object(TestCamera, 'get_frame', side_effect=test_frames) as _:
            # When
            response = self.client.get(ENDPOINTS[VIDEO_FRAME])

            # Validation
            mock_response.assert_called_once_with(test_generator,
                                                  mimetype=MIME_TYPE_MULTIPART_FRAME)
            self.assertEqual(200, response.status_code)
            self.assertEqual(response.is_streamed, True)
            self.assertEqual(response.content_type, MIME_TYPE_MULTIPART_FRAME)
            response_iterator = response.iter_encoded()
            self.assertEqual(next(response_iterator), expected_multipart_frames[0])
            self.assertEqual(next(response_iterator), expected_multipart_frames[1])
            self.assertEqual(next(response_iterator), expected_multipart_frames[2])
            self.assertRaises(RuntimeError, response_iterator.__next__)
            self.assertRaises(StopIteration, response_iterator.__next__)

    @patch('time.sleep')
    @patch('time.time')
    def test_get_video_frame_test_camera_2(self, mock_time: MagicMock, mock_sleep: MagicMock):
        """
        Test the Video stream endpoint
        Test that the same frame is always returned from test camera based on time.time

        :param mock_sleep: mock time.sleep to make test run faster
        :param mock_time: Magic mock of time.time to force the selected frame
        :return:
        """
        # Mock and data
        mock_time.return_value = 3
        test_frames = get_camera_controller().frames
        expected_multipart_frame = Camera._get_multipart_frame(test_frames[0])

        # When
        response = self.client.get(ENDPOINTS[VIDEO_FRAME])

        # Validation
        response_iterator = response.iter_encoded()
        self.assertEqual(next(response_iterator), expected_multipart_frame)
        self.assertEqual(next(response_iterator), expected_multipart_frame)
        self.assertEqual(next(response_iterator), expected_multipart_frame)
