from downloads.database import db
import datetime


class Vote(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cast_for = db.Column(db.String)
    cast_date = db.Column(db.DateTime())

    def __init__(self, *args, **kwargs):
        self.cast_for = kwargs.get('cast_for')
        self.cast_date = datetime.datetime.now()
