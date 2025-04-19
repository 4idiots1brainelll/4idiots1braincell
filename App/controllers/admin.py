from App.database import db
from App.models.admin import Admin

def create_admin(username, password):
    newadmin = Admin(username=username, password=password)
    db.session.add(newadmin)
    db.session.commit()
    return newadmin