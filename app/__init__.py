import os

import sqlalchemy as sa
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    engine = sa.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    inspector = sa.inspect(engine)
    # if not inspector.has_table("users"):
    #     with app.app_context():
    #         db.drop_all()
    #         db.create_all()
    #         app.logger.info("Initialized database")
    # else:   
    #     app.logger.info("Database already contains user table.")
    with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized database")
    
    from .main import main as main_blueprint
    from .main.organizers import organizers_blueprint
    from .main.events import events_blueprint
    from .main.users import users_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(organizers_blueprint)
    app.register_blueprint(events_blueprint)

    return app
