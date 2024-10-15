# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .admin import setup_admin
from .course import course_views
from .allocation import allocation_views
from .home import home_views


views = [user_views, index_views, auth_views,course_views,allocation_views, home_views]
# blueprints must be added to this list