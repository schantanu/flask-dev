# import click
from flask.cli import with_appcontext
from flaskapp import create_app, db
# from flaskapp.models import User

app = create_app()

with app.test_request_context():
     db.init_app(app)
     db.drop_all()
     db.create_all()

# @click.command(name='create_tables')
# @with_appcontext
# def create_tables():
#      db.create_all()

# import click
# from flask.cli import with_appcontext
# from . import create_app, db

# app = create_app()

# @click.command(name='create_tables')
# @with_appcontext
# def create_tables():
#      db.create_all()