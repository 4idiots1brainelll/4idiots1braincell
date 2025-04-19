# Import all blueprints explicitly
from .user import user_views
from .index import index_views
from .auth import auth_views
from .signup import signup_views
from .dashboard import dashboard_views
from .viewreport import viewreport_views
from .download import download_views
from .generate import generate_views
from .upload_sheet import upload_sheet_views
from .admin_uploadTemplate import admin_upload_template_views
from .admin_dashboard import admin_dashboard_views

views = [user_views, index_views, auth_views, signup_views, dashboard_views,download_views,generate_views, upload_sheet_views, viewreport_views, admin_upload_template_views, admin_dashboard_views] 


# blueprints must be added to this list

