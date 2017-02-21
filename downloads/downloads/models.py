from downloads.database import db
import datetime


class Download(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    institution = db.Column(db.String(500))
    scientific_purposes_only = db.Column(db.Boolean)
    requested_date = db.Column(db.DateTime())

    def __init__(self, *args, **kwargs):
        self.title = kwargs.get('title')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.institution = kwargs.get('institution')
        self.scientific_purposes_only = kwargs.get('scientific_purposes_only')
        self.requested_date = datetime.datetime.now()
