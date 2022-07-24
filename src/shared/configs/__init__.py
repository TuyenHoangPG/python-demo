import os
from dotenv import load_dotenv

load_dotenv()
baseDir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDISTOGO_URL = os.getenv("REDISTOGO_URL")
    BCRYPT_LOG_ROUNDS = 4
    TOKEN_EXPIRE_HOURS = 0
    TOKEN_EXPIRE_MINUTES = 0
    SWAGGER_UI_DOC_EXPANSION = "list"
    RESTX_MASK_SWAGGER = False
    JSON_SORT_KEYS = False


class ProductionConfig(Config):
    ENV = "production"
    TOKEN_EXPIRE_HOURS = 1
    BCRYPT_LOG_ROUNDS = 13
    DEBUG = True


class StagingConfig(Config):
    ENV = "staging"
    DEBUG = True


class DevelopmentConfig(Config):
    ENV = "development"
    TOKEN_EXPIRE_MINUTES = 15
    DEBUG = True


class TestingConfig(Config):
    ENV = "development"
    TESTING = True


ENV_CONFIG_DICT = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)


def get_config(config_name):
    """Retrieve environment configuration settings."""
    return ENV_CONFIG_DICT.get(config_name, DevelopmentConfig)
