from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"


def create_database(app) -> None:
    """
    Creating data base if not exists.
    :param app: Flask app
    :return:  -Null-
    """
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created dabatase!")


def init_app(app) -> None:
    """
    Running SQLAlchemy DB server
    :param app: Flask app that use DB
    :return: -Null-
    """
    # from .models import User, Note, Message  # if there will be any errors with DB, now works fine.
    db.init_app(app)
