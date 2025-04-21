from .user import create_user
from .admin import create_admin
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_admin('admin', 'adminpass')
