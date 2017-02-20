import os


class BaseConfig(object):
    """Standard configuration options"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_FILE = os.path.join(BASE_DIR, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILE
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "secret"


class TestConfig(BaseConfig):
    """Configuration for general testing"""
    TESTING = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_FILE = os.path.join(BASE_DIR, 'test.db')
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class TestConfigCRSF(TestConfig):
    WTF_CSRF_ENABLED = True
