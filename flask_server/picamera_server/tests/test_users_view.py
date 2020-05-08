"""
Test the Users view
"""
from picamera_server.models import User
from picamera_server.views.users_view import USER_CREATE_COMMAND, USER_CLI_GROUP, USER_CHANGE_PASSWORD_COMMAND,\
    USER_DELETE_COMMAND
from picamera_server.tests.base_test_class import BaseTestClass
from picamera_server.tests.helpers.user import create_user


class TestUsersView(BaseTestClass):

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
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CREATE_COMMAND, 'admin', 'admin'])

        # Validation
        self.assertEqual(User.query.count(), 1)
        self.assertIn('created', result.output)

    def test_create_user_already_exist_command(self):
        """
        Test create user command when the username already exist

        :return:
        """
        # Data
        username = 'test'
        create_user(username, password=username)

        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CREATE_COMMAND, username, username])

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
                                              username, username, password_2, password_2])

        # Validation
        self.assertIn('Password changed', result.output)
        user = User.query.filter_by(username=username).first_or_404()
        self.assertTrue(user.check_password(password_2))
        self.assertFalse(user.check_password(username))

    def test_user_change_password_invalid_password(self):
        """
        Test change password invalid password input

        :return:
        """
        # Data
        username = 'test'
        create_user(username, password=username)

        # When
        result = self.app_runner.invoke(args=[USER_CLI_GROUP, USER_CHANGE_PASSWORD_COMMAND,
                                              username, 'invalid', 'invalid', 'invalid'])

        # Validation
        self.assertIn('Invalid password', result.output)
        user = User.query.filter_by(username=username).first_or_404()
        self.assertTrue(user.check_password(username))

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
                                              username, username, 'invalid', 'invalid1'])

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
                                              'invalid', 'invalid', 'invalid', 'invalid'])

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
