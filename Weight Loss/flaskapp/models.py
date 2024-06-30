from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

user_challenge = db.Table('user_challenge',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
)

post_challenge = db.Table('post_challenge',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    challenges = db.relationship('Challenge', secondary=user_challenge, backref='users', lazy='select')
 
    # Attributes
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    animal = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=True)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)

    @staticmethod
    def create_admin(animal):
        user = User.query.filter_by(animal=animal).first()
        if user:
            user.role = 'admin'
            print(f"{animal} is now an admin.")
        else:
            print("Animal not found. Please enter another animal.")
        db.session.commit()

    def __repr__(self):
        return f"User ('{self.animal}', '{self.email}')"
 

class Challenge(db.Model):
    __tablename__ = 'challenge'
    id = db.Column(db.Integer, primary_key=True)
    entries = db.relationship('Entry', backref='challenge')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Attributes
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(350), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)


class Entry(db.Model):
    __tablename__ = 'entry'
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Attributes
    enrolled = db.Column(db.Boolean, nullable=False, default=False)
    region = db.Column(db.String(50), nullable=False)
    metric = db.Column(db.String(50), nullable=False)
    current_weight = db.Column(db.Float, nullable=False)
    goal_weight = db.Column(db.Float, nullable=False)
    
    def __repr__(self):
        return f"Entry('{self.user_id}', '{self.date_posted}')"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    challenges = db.relationship('Challenge', secondary=post_challenge, backref='posts', lazy='select')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Attributes
    type = db.Column(db.String(50), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Post('{self.weight}', '{self.date_posted}')"