from flask import Flask, render_template, redirect, url_for
import traceback
from config import BaseConfig
from downloads.forms import DownloadForm
from downloads.database import initialise_db
from downloads import models
from downloads.database import db


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.errorhandler(500)
    @app.errorhandler(Exception)
    def internal_error(exception):
        print(traceback.format_exc())
        app.logger.error(traceback.format_exc())
        return render_template('500.html'), 500

    @app.route('/', methods=['GET', 'POST'])
    def index():
        f = DownloadForm()

        if f.validate_on_submit():

            return redirect(url_for('results'))

        return render_template('details.html', form=f)

    @app.route('/results', methods=['GET', 'POST'])
    def results():
        vs = models.Download.query.all()

        return render_template('results.html', votes=vs)

#    @app.before_first_request
#    def recreate_test_databases():
#        initialise_db(app)

    return app
