from flask_wtf import Form
from wtforms import TextField, BooleanField


class DownloadForm(Form):
    title = TextField(label='Title')
    first_name = TextField(label='First Name')
    last_name = TextField(label='Last Name')
    institution = TextField(label='Institution')
    scientific_purposes_only = BooleanField(
        label='Use of data is for scientific purposes only')
