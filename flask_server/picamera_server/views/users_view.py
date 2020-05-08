import click
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from picamera_server import db, app
from picamera_server.models import User

USER_CLI_GROUP = 'user'

users = Blueprint('users', __name__, cli_group=USER_CLI_GROUP)

USER_CREATE_COMMAND = 'create'
USER_CHANGE_PASSWORD_COMMAND = 'change_password'
USER_DELETE_COMMAND = 'delete'


@users.cli.command(USER_CREATE_COMMAND)
@click.argument('username', required=True)
@click.argument('password', required=True)
def user_create(username: str, password: str):
    """
    Create a user

    :param username:
    :param password:
    :return:
    """
    message = ''
    try:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        message = 'User "{}" created'.format(username)
        app.logger.info(message)
    except IntegrityError as e:
        if 'UNIQUE constraint' in e.orig.args[0]:
            message = 'Error creating user "{}", that username already exist'.format(username)
            app.logger.error('Error creating user "{}", that username already exist'.format(username))
    finally:
        click.echo(message)


@users.cli.command(USER_CHANGE_PASSWORD_COMMAND)
@click.argument('username', required=True)
@click.argument('password', required=True)
@click.argument('new_password', required=True)
@click.argument('new_password_repeat', required=True)
def user_change_password(username: str, password: str, new_password: str, new_password_repeat: str):
    """
    Set a new password to a user

    :param username:
    :param password:
    :param new_password:
    :param new_password_repeat:
    :return:
    """
    message = ''
    try:
        user = User.query.filter_by(username=username).first_or_404()
        if not user.check_password(password):
            raise ValueError('Invalid password')
        if new_password != new_password_repeat:
            raise ValueError("Input passwords don't match")
        user.set_password(new_password)
        db.session.add(user)
        db.session.commit()
        message = 'Password changed for user "{}"'.format(username)
        app.logger.info(message)
    except NotFound:
        message = 'Username "{}" not found'.format(username)
        app.logger.error(message)
    except ValueError as e:
        message = '{} username "{}" not changed'.format(e, username)
        app.logger.error(message)
    finally:
        click.echo(message)


@users.cli.command(USER_DELETE_COMMAND)
@click.argument('username', required=True)
def user_delete(username: str):
    """
    Delete a user

    :param username:
    :return:
    """
    message = ''
    try:
        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        message = 'User "{}" deleted'.format(username)
        app.logger.info(message)
    except NotFound:
        message = 'Username "{}" not found'.format(username)
        app.logger.error(message)
    finally:
        click.echo(message)
