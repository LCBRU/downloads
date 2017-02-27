import os
import logging
from downloads import create_app
from downloads.database import upgrade_db
from config import LiveConfig


def application(environ, start_response):
    for key in ['FLASK_SECRET_KEY', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']:
        os.environ[key] = environ.get(key, '')
        logging.error(os.environ[key])

    app = create_app(LiveConfig)

    with app.app_context():
        upgrade_db(app)

    return app
