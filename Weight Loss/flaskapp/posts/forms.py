from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import FloatField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    weight = FloatField('Weight', validators=[DataRequired()])
    submit = SubmitField('Add')