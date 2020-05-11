from typing import Optional
from picamera_server import app, db
from picamera_server.models import User


def create_user(username: str, password: str) -> Optional[User]:
    """
    Create a user

    :param username:
    :param password:
    :return:
    """
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
