from flask import Blueprint

events_blueprint = Blueprint(
    "events",
    __name__,
    static_folder="../../static",
    template_folder="../../templates",
)

