# Import all blueprints explicitly
from .user import user_views
from .index import index_views
from .auth import auth_views
from .signup import signup_views
from .dashboard import dashboard_views
from .upload_sheet import upload_sheet_views

# List of all views
views = [
    user_views,
    index_views, 
    auth_views,
    signup_views,
    dashboard_views,
    upload_sheet_views
]

# Admin setup function
def setup_admin(app):
    from .admin import setup_admin as admin_setup
    admin_setup(app)