from flask import Blueprint

from .users import routes

main = Blueprint(
    "main",
    __name__,
    static_folder="app/static",
    template_folder="app/templates",
)

from . import errors, forms
