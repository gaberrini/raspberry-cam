from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def config_database(app: Flask) -> SQLAlchemy:
    """
    Config the database in the app
    :param app:
    :return:
    """
    db = SQLAlchemy(app)
    return db
