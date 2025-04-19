from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

from App.models.user import User 

class Admin(User):
    __tablename__ = 'admin'
    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, username, password):
        super().__init__(username, password)  