from flask import Blueprint

# precisa disso porque usa redirecionamento de routes
main = Blueprint('main', __name__)

from .root_routes import *
from .ahp_routes import *
from .dash_routes import *
