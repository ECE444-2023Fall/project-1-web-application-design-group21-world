from flask import Blueprint

organizers_blueprint = Blueprint(
    "organizers",
    __name__,
    static_folder="../../static",
    template_folder="../../templates",
)

from . import routes
