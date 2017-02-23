from flask import flash
from flask_wtf import FlaskForm
from wtforms import TextField, BooleanField
from wtforms.validators import DataRequired, Length, AnyOf


class FlashingForm(FlaskForm):
    def validate_on_submit(self):
        result = super(FlashingForm, self).validate_on_submit()

        if not result:
            for field, errors in self.errors.items():
                for error in errors:
                    flash(
                        u"Error in the %s field - %s" %
                        (getattr(self, field).label.text, error),
                        'error')
        return result


class DownloadForm(FlashingForm):
    title = TextField(label='Title', validators=[
                      DataRequired(), Length(max=50)])
    first_name = TextField(label='First Name', validators=[
                           DataRequired(), Length(max=100)])
    last_name = TextField(label='Last Name', validators=[
                          DataRequired(), Length(max=100)])
    institution = TextField(label='Institution', validators=[
                            DataRequired(), Length(max=500)])
    scientific_purposes_only = BooleanField(
        label='Use of data is for scientific purposes only',
        validators=[AnyOf(
                    [True],
                    'Please confirm that the data is for use '
                    'for scientic purposes only')])
