import os
import datetime
import traceback
from multiprocessing import Lock
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


dbUpgradeDir = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'db_upgrade'
)
lock = Lock()


def initialise_db(app):
    db.init_app(app)
