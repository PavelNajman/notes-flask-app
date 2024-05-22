import os
import secrets


class Config:
    # flask
    SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(16))

    # smorest
    API_TITLE = "Notes API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"

    # sqlalchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.sqlite"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///test.sqlite"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", "sqlite:///data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
