from downloads import create_app
from downloads.database import upgrade_db
from config import LiveConfig

application = create_app(LiveConfig)

with application.app_context():
    upgrade_db(application)
