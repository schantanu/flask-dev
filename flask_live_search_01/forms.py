from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import Optional, InputRequired

# class NonValidatingSelectField(SelectField):
#     """
#     Attempt to make an open ended select multiple field that can accept dynamic
#     choices added by the browser.
#     """
#     def pre_validate(self, form):
#         pass

class InputForm(FlaskForm):
    # states = NonValidatingSelectField("US States")
    states = SelectField("US States", validate_choice=False)
    territory = SelectField("Is Territory?", choices=["Yes", "No"], validators=[InputRequired()])
    submit = SubmitField("Add State", validators=[Optional()])