from picamera_server.config.database import DB_INSTANCE

print('import')


class User(DB_INSTANCE.Model):
    id = DB_INSTANCE.Column(DB_INSTANCE.Integer, primary_key=True)
    username = DB_INSTANCE.Column(DB_INSTANCE.String(80), unique=True, nullable=False)
    email = DB_INSTANCE.Column(DB_INSTANCE.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
