import click
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from picamera_server import db, app, login_manager
from picamera_server.models import User
from picamera_server.forms.logging_form import LoginForm

USER_CLI_GROUP = 'user'

users = Blueprint('users', __name__, cli_group=USER_CLI_GROUP)

USER_CREATE_COMMAND = 'create'
USER_CHANGE_PASSWORD_COMMAND = 'change_password'
USER_DELETE_COMMAND = 'delete'

USER_LOGIN = 'login'
USER_LOGOUT = 'logout'
ENDPOINTS = {
    USER_LOGIN: '/login',
    USER_LOGOUT: '/logout'
}

TEMPLATES = {
    USER_LOGIN: 'login.html'
}


@users.route(ENDPOINTS[USER_LOGIN], methods=['POST', 'GET'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('home.ui_home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('users.user_login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home.ui_home'))

    return render_template(TEMPLATES[USER_LOGIN], form=form)


@users.route(ENDPOINTS[USER_LOGOUT], methods=['GET'])
def user_logout():
    logout_user()
    return redirect(url_for('users.user_login'))


@login_manager.user_loader
def load_user(user_id: str) -> User:
    """
    Load the user to be used by the LoginManager
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))


@users.cli.command(USER_CREATE_COMMAND)
@click.argument('username', required=True)
@click.argument('password', required=True)
@click.argument('password_repeat', required=True)
def user_create(username: str, password: str, password_repeat: str):
    """
    Create a user

    :param username:
    :param password:
    :param password_repeat:
    :return:
    """
    message = ''
    try:
        if password != password_repeat:
            message = "Input passwords don't match"
            raise ValueError(message)

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
    except ValueError:
        pass
    finally:
        click.echo(message)


@users.cli.command(USER_CHANGE_PASSWORD_COMMAND)
@click.argument('username', required=True)
@click.argument('new_password', required=True)
@click.argument('new_password_repeat', required=True)
def user_change_password(username: str, new_password: str, new_password_repeat: str):
    """
    Set a new password to a user

    :param username:
    :param new_password:
    :param new_password_repeat:
    :return:
    """
    message = ''
    try:
        user = User.query.filter_by(username=username).first_or_404()
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
