from datetime import datetime
import enum
from application import db #, login_manager
# from flask_login import UserMixin

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class User(db.Model):
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)
#     first_name = db.Column(db.String(30), nullable=False)
#     last_name = db.Column(db.String(30), nullable=False)
#     timezone = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}', '{self.image_file}')"

# class Participant(db.Model):
    
#     # id = 
#     # unit = 
#     age = db.Column(db.Integer, nullable=False)
#     height_ft = db.Column(db.Integer, nullable=False)
#     height_inch = db.Column(db.Integer, nullable=False)
#     weight_current = db.Column(db.Float, nullable=False)
#     weight_goal = db.Column(db.Float, nullable=False)
#     seed = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"

class IncomeExpenses(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30), default = 'income', nullable=False)
    category = db.Column(db.String(30), nullable=False, default='rent')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

