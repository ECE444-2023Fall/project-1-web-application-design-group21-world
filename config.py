import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    def init_app(app):
        pass
    pass

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    pass

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
    }