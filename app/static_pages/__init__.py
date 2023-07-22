from flask import Blueprint

static_pages = Blueprint("static_pages", __name__)

from . import views