from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import g

from flaskapp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'primary'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        if db not in g:
            db.create_all()
    
    from flaskapp.main.routes import main
    from flaskapp.posts.routes import posts
    from flaskapp.users.routes import users
    from flaskapp.errors.handlers import errors
    from flaskapp.challenge.routes import challenge
    from flaskapp.commands import setup_db, setup_admin
    
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)
    app.register_blueprint(challenge)

    app.cli.add_command(setup_db) 
    app.cli.add_command(setup_admin)

    app.jinja_env.add_extension('jinja2.ext.do')

    return app
