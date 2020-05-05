"""
Test camera view
"""
import sys
import io
from unittest.mock import patch, MagicMock
from importlib import reload
from flask import Response

import picamera_server.views.utils.camera.pi_camera as picamera
from picamera_server.models import CapturedImage
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.views.camera_view import ENDPOINTS, VIDEO_FRAME, MIME_TYPE_MULTIPART_FRAME, get_camera_controller
from picamera_server.views.utils.camera.base_camera import Camera
from picamera_server.views.utils.camera.test_camera import TestCamera
from picamera_server.views.utils.camera.camera_controllers import set_camera_class, init_camera_controller
from picamera_server.views.utils.camera.pi_camera import PiCamera


class TestPiCamera(BaseTestClass):

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Clean up the mocks, go back camera class to TestCamera

        :return:
        """
        cls._clean_up_mock_picamera()
        set_camera_class(TestCamera)
        init_camera_controller()
        super(TestPiCamera, cls).tearDownClass()

    @classmethod
    def setUpClass(cls) -> None:
        """
        Mock picamera

        :return:
        """
        # Set modules patch and reload module
        cls._mock_picamera()
        reload(picamera)
        set_camera_class(PiCamera)
        init_camera_controller()
        cls.mock_picamera = sys.modules['picamera']
        super(TestPiCamera, cls).setUpClass()

    @classmethod
    def _mock_picamera(cls):
        """
        Mock picamera module and set them up to sys modules
        :return:
        """
        cls.mock_picamera_module = MagicMock()
        cls.mock_picamera_class = MagicMock()
        cls.mock_picamera_class.capture = MagicMock()
        cls.mock_picamera_class.capture.side_effect = TestPiCamera._mock_camera_capture
        cls.mock_pi_camera_exc = MagicMock()
        cls.mock_picamera_module.PiCamera = MagicMock()
        cls.mock_picamera_module.PiCamera.return_value = cls.mock_picamera_class
        sys.modules['picamera'] = cls.mock_picamera_module
        sys.modules['picamera.exc'] = cls.mock_pi_camera_exc

    @staticmethod
    def _clean_up_mock_picamera():
        """
        Clean up mocks created by _mock_picamera
        :return:
        """
        TestPiCamera._try_clean_up_module('picamera')
        TestPiCamera._try_clean_up_module('picamera.exc.PiCameraMMALError')

    @staticmethod
    def _try_clean_up_module(module_name: str) -> None:
        """
        Try to delete a module from the sys modules, ignore errors.
        :param module_name:
        :return:
        """
        try:
            del(sys.modules[module_name])
        except KeyError:
            pass

    @staticmethod
    def _mock_camera_capture(stream: io.BytesIO, format: str) -> None:
        """
        Write a test frame in the stream to mock the picamera.PiCamera.capture method

        :param stream: BytesIO open stream
        :param format: data format
        :return:
        """
        stream.write(TestCamera().get_frame())

    @patch('picamera_server.views.camera_view.stream_with_context')
    @patch('picamera_server.views.camera_view.Response')
    def test_get_video_frame_test_camera(self, mock_response: MagicMock, mock_stream_with_context: MagicMock):
        """
        Test the Video stream endpoint,
        Create a list of expected frames and then StopIteration

        :param mock_response: Magic mock of flask Response
        :param mock_stream_with_context: Magic mock of flask stream_with_context
        :return:
        """
        # Mock and data
        test_generator = get_camera_controller().frames_generator()
        test_frames = TestCamera().frames

        mock_stream_with_context.return_value = test_generator
        mock_response.side_effect = Response

        expected_multipart_frames = [Camera._get_multipart_frame(test_frames[0]),
                                     Camera._get_multipart_frame(test_frames[1]),
                                     Camera._get_multipart_frame(test_frames[2])]

        # Get frame of TestCamera is used in the _mock_camera_capture method
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

    def test_camera_close(self):
        """
        Test the camera close method
        :return:
        """
        # When
        get_camera_controller()._close_camera()

        # Validation
        self.mock_picamera_class.close.assert_called_once()
