from downloads import create_app
from downloads.database import upgrade_db
from config import LiveConfig

app = create_app(LiveConfig)

with app.app_context():
    upgrade_db(app)
