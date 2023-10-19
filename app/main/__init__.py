from flask import Blueprint

main = Blueprint("main", __name__, static_folder="app/static", template_folder="app/templates")

from . import errors, views
