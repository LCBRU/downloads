from downloads import create_app
from downloads.database import upgrade_db

application = create_app()

with application.app_context():
    upgrade_db(application)
