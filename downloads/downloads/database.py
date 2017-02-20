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

    app.logger.info('Upgrading DB')

    with lock:
        db.engine.execute("""
            CREATE TABLE IF NOT EXISTS db_version (
            id INT AUTO_INCREMENT,
            version INT,
            appliedDate DATETIME,
            PRIMARY KEY(id));
        """)
        currentVersion = db.engine.execute("""
            SELECT MAX(version) maxVersion
            FROM db_version
        """).fetchall()[0][0] or 0

        app.logger.info('Upgrading DB from version %d' % currentVersion)

        upgradeScripts = [f for f in os.listdir(dbUpgradeDir)
                          if f.split('.')[0].isdigit() and
                          f.split('.')[1] == 'sql' and
                          os.path.isfile(os.path.join(dbUpgradeDir, f)) and
                          int(f.split('.')[0]) > currentVersion]

        upgradeScripts.sort(key=lambda s: int(s.split('.')[0]))

        for f in upgradeScripts:
            app.logger.info('Running DB script %s' % f)

            with open(os.path.join(dbUpgradeDir, f)) as s:
                try:
                    db.engine.execute(s.read())

                    db.engine.execute("""
                        INSERT INTO db_version (version, appliedDate)
                        VALUES (:version, :applied_date)
                        """, {
                        'version': int(f.split('.')[0]),
                        'applied_date': datetime.datetime.now()
                    })
                except:
                    app.logger.error(traceback.format_exc())
                    db.engine.raw_connection().cursor().execute("ROLLBACK;")
                    raise
