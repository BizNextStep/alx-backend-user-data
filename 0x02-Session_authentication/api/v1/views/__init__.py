#!/usr/bin/env python3
"""
This module sets up the Flask Blueprint for the application views.
It imports the necessary modules and ensures user data is loaded on startup.
"""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import routes to register with the blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load user data from file
User.load_from_file()

