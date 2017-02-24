from downloads import create_app
from downloads.database import upgrade_db

app = create_app()

with app.app_context():
    upgrade_db(app)
