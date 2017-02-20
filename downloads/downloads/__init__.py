from flask import Flask, render_template, redirect, url_for
import traceback
from config import BaseConfig
from hvc.forms import VoteForm
from hvc.database import initialise_db
from hvc import models
from hvc.database import db


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
        f = VoteForm()

        if f.validate_on_submit():
            v = models.Vote(cast_for='H')

            db.session.add(v)
            db.session.commit()

            return redirect(url_for('results'))

        return render_template('vote.html', form=f)

    @app.route('/results', methods=['GET', 'POST'])
    def results():
        vs = models.Vote.query.all()

        return render_template('results.html', votes=vs)

    @app.before_first_request
    def recreate_test_databases():
        initialise_db(app)

    return app
