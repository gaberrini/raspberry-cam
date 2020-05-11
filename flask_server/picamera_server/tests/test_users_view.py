"""
Test the Users view
"""
from flask import url_for, render_template
from flask.wrappers import Response
from unittest.mock import patch, MagicMock
from picamera_server.models import User
from picamera_server.views.users_view import USER_CREATE_COMMAND, USER_CLI_GROUP, USER_CHANGE_PASSWORD_COMMAND,\
    USER_DELETE_COMMAND, TEMPLATES, USER_LOGIN
from picamera_server.forms.logging_form import LoginForm
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.tests.helpers.user import create_user


class TestUsersCommands(BaseTestClass):

    def setUp(self) -> None:
        self.db.create_all()

    def tearDown(self) -> None:
        self.db.session.remove()
        self.db.drop_all()

    def test_create_user_command(self):
        """
        Test create user command

        :return:
        """
        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CREATE_COMMAND, 'admin', 'admin', 'admin'])

        # Validation
        self.assertEqual(User.query.count(), 1)
        self.assertIn('created', result.output)

    def test_create_user_command_password_repeat_invalid(self):
        """
        Test create user command

        :return:
        """
        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CREATE_COMMAND, 'admin', 'admin', 'admin2'])

        # Validation
        self.assertEqual(User.query.count(), 0)
        self.assertIn("Input passwords don't match", result.output)

    def test_create_user_already_exist_command(self):
        """
        Test create user command when the username already exist

        :return:
        """
        # Data
        username = 'test'
        create_user(username, password=username)

        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CREATE_COMMAND, username, username, username])

        # Validation
        self.assertEqual(User.query.count(), 1)
        self.assertIn('already exist', result.output)

    def test_user_change_password(self):
        """
        Test change password successfully

        :return:
        """
        # Data
        username = 'test'
        password_2 = 'test2'
        create_user(username, password=username)

        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CHANGE_PASSWORD_COMMAND,
                                              username, password_2, password_2])

        # Validation
        self.assertIn('Password changed', result.output)
        user = User.query.filter_by(username=username).first_or_404()
        self.assertTrue(user.check_password(password_2))
        self.assertFalse(user.check_password(username))

    def test_user_change_password_no_match(self):
        """
        Test change password invalid password input, password don't match

        :return:
        """
        # Data
        username = 'test'
        create_user(username, password=username)

        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CHANGE_PASSWORD_COMMAND,
                                              username, 'invalid', 'invalid1'])

        # Validation
        self.assertIn("passwords don't match", result.output)
        user = User.query.filter_by(username=username).first_or_404()
        self.assertTrue(user.check_password(username))

    def test_user_change_password_user_not_found(self):
        """
        Test change password invalid username

        :return:
        """
        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CHANGE_PASSWORD_COMMAND,
                                              'invalid', 'invalid', 'invalid'])

        # Validation
        self.assertIn("not found", result.output)

    def test_user_delete(self):
        """
        Test delete user successfully

        :return:
        """
        # Data
        username = 'test'
        create_user(username, password=username)

        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_DELETE_COMMAND,
                                              username])

        # Validation
        self.assertIn("deleted", result.output)
        self.assertEqual(User.query.count(), 0)

    def test_user_delete_not_found(self):
        """
        Test delete user, invalid username

        :return:
        """
        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_DELETE_COMMAND,
                                              'invalid'])

        # Validation
        self.assertIn("not found", result.output)


class TestUserLogin(BaseTestClass):

    def setUp(self) -> None:
        """
        Set up testing env
        :return:
        """
        self.db.create_all()
        self.app.config['LOGIN_DISABLED'] = False

    def tearDown(self) -> None:
        """
        Clean up test env
        :return:
        """
        self.db.session.remove()
        self.db.drop_all()
        self.app.config['LOGIN_DISABLED'] = True

    def _assert_login_required(self, response: Response):
        """
        Assert that response required login

        :param response:
        :return:
        """
        self.assertEqual(302, response.status_code)
        self.assertIn('href="{}'.format(url_for('users.user_login')), str(response.data))

    def test_home_view_login_required(self):
        """
        Home view should need user logged in
        :return:
        """
        # When
        response = self.client.get(url_for('home.ui_home'))

        # Validation
        self._assert_login_required(response)

    def test_camera_view_login_required(self):
        """
        Camera view login required test
        :return:
        """
        # When
        response = self.client.get(url_for('camera.ui_camera_stream'))
        response_2 = self.client.get(url_for('camera.video_frame'))

        # Validation
        self._assert_login_required(response)
        self._assert_login_required(response_2)

    def test_captures_mode_view_login_required(self):
        """
        Captures mode view login required test
        :return:
        """
        # When
        response = self.client.get(url_for('capture_mode.ui_config_capture_mode'))
        response_2 = self.client.post(url_for('capture_mode.set_capt_interval_value'))
        response_3 = self.client.post(url_for('capture_mode.set_status_capture_mode'))
        response_4 = self.client.post(url_for('capture_mode.remove_all_captures'))
        response_5 = self.client.get(url_for('capture_mode.ui_captures_paginated'))
        response_6 = self.client.get(url_for('capture_mode.get_captured_image'))

        # Validation
        self._assert_login_required(response)
        self._assert_login_required(response_2)
        self._assert_login_required(response_3)
        self._assert_login_required(response_4)
        self._assert_login_required(response_5)
        self._assert_login_required(response_6)

    def test_user_login(self):
        """
        Test user login
        :return:
        """
        # Mock and data
        test_user = 'test_user'
        create_user(test_user, password=test_user)
        data = {'username': test_user, 'password': test_user}

        # When
        response_login = self.client.post(url_for('users.user_login'), data=data)

        # Validation
        self.assertEqual(302, response_login.status_code)
        self.assertIn('href="{}'.format(url_for('home.ui_home')), str(response_login.data))

    def test_user_logout(self):
        """
        Test user logout
        :return:
        """
        # Mock and data
        test_user = 'test_user_2'
        create_user(test_user, password=test_user)
        data = {'username': test_user, 'password': test_user}

        # When
        response_login = self.client.post(url_for('users.user_login'), data=data)
        response_logout = self.client.get(url_for('users.user_logout'))

        # Validation
        self.assertEqual(302, response_login.status_code)
        self.assertIn('href="{}'.format(url_for('home.ui_home')), str(response_login.data))
        self._assert_login_required(response_logout)

    def test_user_login_invalid_pass(self):
        """
        Test user login
        :return:
        """
        # Mock and data
        test_user = 'test_user_3'
        create_user(test_user, password=test_user)
        data = {'username': test_user, 'password': 'invalid'}

        # When
        self.client.get(url_for('users.user_logout'))
        response_login = self.client.post(url_for('users.user_login'), data=data)

        # Validation
        self._assert_login_required(response_login)

    def test_user_login_already_logged(self):
        """
        Test user login
        :return:
        """
        # Mock and data
        test_user = 'test_user_4'
        create_user(test_user, password=test_user)
        data = {'username': test_user, 'password': test_user}

        # When
        self.client.get(url_for('users.user_logout'))
        self.client.post(url_for('users.user_login'), data=data)
        response_login = self.client.post(url_for('users.user_login'), data=data)

        # Validation
        self.assertEqual(302, response_login.status_code)
        self.assertIn('href="{}'.format(url_for('home.ui_home')), str(response_login.data))

    @patch('picamera_server.views.users_view.render_template')
    @patch('picamera_server.views.users_view.LoginForm')
    def test_get_user_login(self, mock_login_form: MagicMock, mock_render_template: MagicMock):
        """
        Test user login
        :param mock_render_template: Mock render_template
        :return:
        """
        # Mock
        form_mock = LoginForm()
        mock_render_template.side_effect = render_template
        mock_login_form.return_value = form_mock
        mock_login_form.vallidate_on_submit.return_value = False

        # When
        response_login = self.client.get(url_for('users.user_login'))

        # Validation
        self.assertEqual(200, response_login.status_code)
        mock_render_template.assert_called_once_with(TEMPLATES[USER_LOGIN], form=form_mock)
