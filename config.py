import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    IMAGE_PATH = os.environ.get("IMAGE_PATH") or "app/static/assets"
    IMAGE_PATH_EVENTS = os.environ.get("IMAGE_PATH_EVENTS") or "app/static/assets/events"
    IMAGE_PATH_ORGANIZERS = os.environ.get("IMAGE_PATH_ORGANIZERS") or "app/static/assets/organizers"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "data/data-dev.sqlite"
    )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "data/data-test.sqlite"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(
        basedir, "data/data.sqlite"
    )


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
