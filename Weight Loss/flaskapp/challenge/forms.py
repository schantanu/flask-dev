from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import SubmitField, SelectField, FloatField, IntegerField, DateField, StringField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

class CreateChallengeForm(FlaskForm):
    name = StringField('Challenge Name', validators=[DataRequired()])
    type = SelectField('Choose Challenge Type', choices=[('Weight Loss','Weight Loss')],
                         default='Weight Loss', validators=[DataRequired()])
    description = TextAreaField('Challenge Description', validators=[DataRequired()])
    start_date = DateField('Choose Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('Choose End Date', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_start_date(self, start_date):
        today = datetime.today().strftime('%Y-%m-%d')
        start_date = self.start_date.data.strftime('%Y-%m-%d')

        if start_date < today:
            raise ValidationError('The Challenge start date cannot be in the past.')

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        if self.end_date.data < self.start_date.data:
            self.end_date.errors.append('The end date for the Challenge cannot be earlier than start date.')
            return False

        challenge_length = (self.end_date.data - self.start_date.data).days
        if challenge_length > 100:
            self.end_date.errors.append('Challenge are restricted to max of 100 days. Choose an earlier end date.')
            return False

        return True

class JoinChallengeForm(FlaskForm):
    region = SelectField('Choose Region', choices=[('Asia/Kolkata','India'),('US/Central','USA')], default='India', validators=[DataRequired()])
    metric = SelectField('Choose Metric', choices=[('kgs', 'Kilograms'), ('lbs', 'Pounds')], default='Kilograms', validators=[DataRequired()])
    current_weight = FloatField('Current Weight', validators=[DataRequired()])
    goal_weight = FloatField('Goal Weight', validators=[DataRequired()])
    height_ft = IntegerField('Height (ft)', validators=[DataRequired()])
    height_in = FloatField('Height (in)', validators=[DataRequired()])
    submit = SubmitField('Submit')
