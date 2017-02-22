import os


class BaseConfig(object):
    """Standard configuration options"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, 'files')
    SQLALCHEMY_DATABASE_URI = 'mysql://testuser:tester@mysql/downloads'
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "secret"


class TestConfig(BaseConfig):
    """Configuration for general testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:n0fwtj!@localhost/fred'
    WTF_CSRF_ENABLED = False


class TestConfigCRSF(TestConfig):
    WTF_CSRF_ENABLED = True
