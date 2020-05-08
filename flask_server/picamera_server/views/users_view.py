import click
from flask import Blueprint
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from picamera_server import db, app
from picamera_server.models import User


users = Blueprint('users', __name__, cli_group='user')


@users.cli.command('create')
@click.argument('username', required=True)
@click.argument('password', required=True)
def create(username: str, password: str):
    """
    Create a user

    :param username:
    :param password:
    :return:
    """
    try:
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        app.logger.info('User "{}" created'.format(username))
    except IntegrityError as e:
        if 'UNIQUE constraint' in e.orig.args[0]:
            app.logger.error('Error creating user "{}", that username already exist'.format(username))


@users.cli.command('change_password')
@click.argument('username', required=True)
@click.argument('password', required=True)
@click.argument('new_password', required=True)
@click.argument('new_password_repeat', required=True)
def change_password(username: str, password: str, new_password: str, new_password_repeat: str):
    """
    Set a new password to a user

    :param username:
    :param password:
    :param new_password:
    :param new_password_repeat:
    :return:
    """
    try:
        user = User.query.filter_by(username=username).first_or_404()
        if not user.check_password(password):
            raise ValueError('Invalid password')
        if new_password != new_password_repeat:
            raise ValueError("Input passwords don't match")
        user.set_password(new_password)
        db.session.add(user)
        db.session.commit()
        app.logger.info('Password changed for user "{}"'.format(username))
    except IntegrityError as e:
        if 'UNIQUE constraint' in e.orig.args[0]:
            app.logger.error('Error creating user "{}", that username already exist'.format(username))
    except NotFound:
        app.logger.error('Username "{}" not found'.format(username))
    except ValueError as e:
        app.logger.error('{} username "{}" not changed'.format(e, username))


@users.cli.command('delete')
@click.argument('username', required=True)
def change_password(username: str):
    """
    Delete a user

    :param username:
    :return:
    """
    try:
        user = User.query.filter_by(username=username).first_or_404()
        db.session.delete(user)
        db.session.commit()
        app.logger.info('User "{}" deleted'.format(username))
    except NotFound:
        app.logger.error('Username "{}" not found'.format(username))
