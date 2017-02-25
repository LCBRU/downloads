import os
import logging


class LiveConfig(object):
    """configuration options for live
        environment variables are set in Apache http.conf
    """
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', '')
    DEBUG = False
    DB_NAME = os.getenv('DB_NAME', '')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASS = os.getenv('DB_PASSWORD', '')
    SQLALCHEMY_DATABASE_URI = 'mysql://{0}:{1}@localhost/{2}'.format(
        DB_USER, DB_PASS, DB_NAME
    )
    logging.error('HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH')
    print(SQLALCHEMY_DATABASE_URI)
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DOWNLOAD_DIR = os.path.join(BASE_DIR, 'files')
    WTF_CSRF_ENABLED = True


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
