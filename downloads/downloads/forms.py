from flask_wtf import FlaskForm
from wtforms import SubmitField


class VoteForm(FlaskForm):
    humans = SubmitField(label='Humans')
    computers = SubmitField(label='Computers')
