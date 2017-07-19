"""
Initialize the main blueprint
"""
from flask import Blueprint


bp = Blueprint('main', __name__)

from . import views
