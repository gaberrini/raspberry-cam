from werkzeug.security import generate_password_hash, check_password_hash
from picamera_server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password: str) -> None:
        """
        Set the password of the user, hash it before store to database
        :param password:
        :return:
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Check if the password is the hashed password
        :param password:
        :return:
        """
        return check_password_hash(self.password_hash, password)
