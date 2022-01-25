from application.util import generate

class Config(object):
    SECRET_KEY = generate(50)
    UPLOAD_FOLDER = '/app/application/static/petpets'
    MAX_CONTENT_LENGTH = 2.5 * 1000 * 1000

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True