from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms import validators
from wtforms.validators import Optional, InputRequired, DataRequired, AnyOf, ValidationError

US_STATES = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California",
             "Colorado", "Connecticut", "District ", "of Columbia", "Delaware",
             "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois",
             "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland",
             "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana",
             "North Carolina", "North Dakota", "Nebraska", "New Hampshire",
             "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma",
             "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina",
             "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands",
             "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]


def get_us_states_from_api():
    return US_STATES


def states_validator(form, field):
    if field.data not in get_us_states_from_api():
        raise ValidationError('Please choose the right state')


class InputForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    states = StringField("US States", validators=[DataRequired(), states_validator])
    territory = SelectField("Is Territory?", choices=["Unknown", "Yes", "No"], default="Unknown", validators=[InputRequired()])
    submit = SubmitField("Add State", validators=[Optional()])
