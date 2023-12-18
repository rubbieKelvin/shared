# See docs at shared/README.md

__version__ = "0.0.0"
__author__ = {"name": "Rubbie kelvin", "email": "dev.rubbie@gmail.com"}

# shortcuts
from .view_tools.paths import Api
from .view_tools.pagination import paginate_by_queryparam
from .view_tools.body_tools import validate, get_validated_body