from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB_INSTANCE = None


def config_database(app: Flask) -> None:
    """
    Config the database in the app
    :param app:
    :return:
    """
    global DB_INSTANCE
    DB_INSTANCE = SQLAlchemy(app)

    # DB_INSTANCE.create_all()
    # admin = User(username='admin', email='admin@example.com')
    # try:
    #     DB_INSTANCE.session.add(admin)
    #
    #     DB_INSTANCE.session.commit()
    # except Exception as e:
    #     print('exception')
    # DB_INSTANCE.session.remove()
    # users = User.query.all()
    # print(users)


def get_db_instance() -> SQLAlchemy:
    """
    Return global DB_INSTANCE

    :return:
    """
    return DB_INSTANCE
