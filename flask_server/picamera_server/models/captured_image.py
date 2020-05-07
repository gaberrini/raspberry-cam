import datetime
from picamera_server import db


class CapturedImage(db.Model):
    """
    Captured image.

    Fields:
        - relative_path: Relative path of the stored file based on the CAPTURES_DIR that was configured when the
        capture was created
        - created_at: date of creation
    """
    id = db.Column(db.Integer, name='id', primary_key=True, autoincrement=True)
    relative_path = db.Column(db.String(255), name='relative_path', nullable=False, unique=True)
    created_at = db.Column(db.DateTime, name='created_at', nullable=False, default=datetime.datetime.now)
