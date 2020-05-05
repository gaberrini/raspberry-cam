import datetime
from picamera_server import db


class CapturedImage(db.Model):
    """
    Captured image stored in the database
    """
    id = db.Column(db.Integer, name='id', primary_key=True, autoincrement=True)
    image = db.Column(db.LargeBinary, name='image', nullable=False)
    created_at = db.Column(db.DateTime, name='created_at', nullable=False, default=datetime.datetime.now)
