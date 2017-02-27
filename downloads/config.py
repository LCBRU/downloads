import os
import logging


class LiveConfig(object):
    """configuration options for live
        environment variables are set in Apache http.conf
    """

    def __init__(self):
        self.SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'NOT SET')
        self.DEBUG = False
        self.DB_NAME = os.getenv('DB_NAME', 'NOT SET')
        self.DB_USER = os.getenv('DB_USER', 'NOT SET')
        self.DB_PASS = os.getenv('DB_PASSWORD', 'NOT SET')
        self.SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@127.0.0.1/{2}'.format(
            self.DB_USER, self.DB_PASS, self.DB_NAME
        )
        logging.error(self.SQLALCHEMY_DATABASE_URI)
        self.BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        self.DOWNLOAD_DIR = os.path.join(self.BASE_DIR, 'files')
        self.WTF_CSRF_ENABLED = True


class BaseConfig(object):
    """configuration options for dev docker instances"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, 'files')
    SQLALCHEMY_DATABASE_URI = 'mysql://testuser:tester@mysql/downloads'
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "secret"


class TestConfig(BaseConfig):
    """Configuration for general testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False


class TestConfigCRSF(BaseConfig):
    WTF_CSRF_ENABLED = True
