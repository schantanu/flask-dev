from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from flaskapp.models import User

animals = ['Anaconda', 'Ant', 'Anteater', 'Antelope', 'Aphid', 'Armadillo', 'Asp', 'Ass',
        'Baboon', 'Badger', 'Bald Eagle', 'Barracuda', 'Bass', 'Basset Hound', 'Bat', 
        'Bearded Dragon', 'Beaver', 'Bedbug', 'Bee', 'Bee-eater', 'Bird', 'Bison', 
        'Black panther', 'Black Widow Spider', 'Blue Jay', 'Blue Whale', 'Bobcat', 
        'Buffalo', 'Butterfly', 'Buzzard', 'Camel', 'Canada Lynx', 'Carp', 'Cat', 
        'Caterpillar', 'Catfish', 'Cheetah', 'Chicken', 'Chimpanzee', 'Chipmunk', 
        'Cobra', 'Cod', 'Condor', 'Cougar', 'Cow', 'Coyote', 'Crab', 'Crane Fly', 
        'Cricket', 'Crocodile', 'Crow', 'Cuckoo', 'Deer', 'Dinosaur', 'Dog', 'Dolphin', 
        'Donkey', 'Dove', 'Dragonfly', 'Duck', 'Eagle', 'Eel', 'Elephant', 'Emu', 'Falcon', 
        'Ferret', 'Finch', 'Fish', 'Flamingo', 'Flea', 'Fly', 'Fox', 'Frog', 'Goat', 'Goose', 
        'Gopher', 'Gorilla', 'Guinea Pig', 'Hamster', 'Hare', 'Hawk', 'Hippopotamus', 'Horse', 
        'Hummingbird', 'Humpback Whale', 'Husky', 'Iguana', 'Impala', 'Kangaroo', 'Lemur', 
        'Leopard', 'Lion', 'Lizard', 'Llama', 'Lobster', 'Margay', 'Monitor lizard', 'Monkey', 
        'Moose', 'Mosquito', 'Moth', 'Mountain Zebra', 'Mouse', 'Mule', 'Octopus', 'Orca', 
        'Ostrich', 'Otter', 'Owl', 'Ox', 'Oyster', 'Panda', 'Parrot', 'Peacock', 'Pelican', 
        'Penguin', 'Perch', 'Pheasant', 'Pig', 'Pigeon', 'Polar bear', 'Porcupine', 'Quagga',
        'Rabbit', 'Raccoon', 'Rat', 'Rattlesnake', 'Red Wolf', 'Rooster', 'Seal', 'Sheep', 
        'Skunk', 'Sloth', 'Snail', 'Snake', 'Spider', 'Tiger', 'Whale', 'Wolf', 'Wombat', 'Zebra']


def get_animal():
    x = [(c, c) for c in animals]
    return x

class RegistrationForm(FlaskForm):
    animal = SelectField('Choose Animal', choices=get_animal(), validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_animal(self, animal):
        user = User.query.filter_by(animal=animal.data).first()
        if user:
            raise ValidationError('Animal is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please login using email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    animal = StringField('Choose Animal', validators=[Optional()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    # def validate_animal(self, animal):
    #     if animal.data != current_user.animal:
    #         user = User.query.filter_by(animal=animal.data).first()
    #         if user:
    #             raise ValidationError('That animal is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')