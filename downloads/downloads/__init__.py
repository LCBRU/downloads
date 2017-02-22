from flask import Flask, render_template, redirect, url_for
from flask import send_from_directory
import traceback
from config import BaseConfig
from downloads.forms import DownloadForm
from downloads.database import initialise_db, db
from downloads.models import Download


def create_app(config=BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)

    with app.app_context():
        initialise_db(app)

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
            d = Download(
                title=f.title.data,
                first_name=f.first_name.data,
                last_name=f.last_name.data,
                institution=f.institution.data,
                scientific_purposes_only=f.scientific_purposes_only.data
            )

            db.session.add(d)
            db.session.commit()

            return redirect(
                url_for('submitted', id=d.id))

        return render_template('details.html', form=f)

    @app.route('/submitted/<string:id>')
    def submitted(id):
        d = Download.query.get_or_404(id)
        return render_template('submitted.html', id=d.id)

    @app.route('/download/<string:id>')
    def download(id):
        Download.query.get_or_404(id)
        return send_from_directory(
            app.config['DOWNLOAD_DIR'],
            'ENGAGE_telo_overall_finalrelease.zip',
            as_attachment=True,
            attachment_filename='ENGAGE_telo_overall_finalrelease.zip'
        )

    return app
