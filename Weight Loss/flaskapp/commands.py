# import click
# from flask import Blueprint

# bp = Blueprint('students', __name__, cli_group=None)

# @bp.cli.command('create')
# @click.argument('name')
# def create(name):
#     print("Registering", name)

import click
from flask.cli import with_appcontext
from . import db
from .models import User

@click.command(name='setup_db')
@with_appcontext
def setup_db():
    db.create_all()

@click.command(name='setup_admin')
@click.argument('animal')
@with_appcontext
def setup_admin(animal):
    animal = animal.capitalize()
    try:
        User.create_admin(animal)
        # print("Animal is", animal)
    except Exception as e:
        print(e)


# def assign_admin_role(animal):
#     with app.app_context():
#         db.init_app(app)
#         try:
#             User.create_admin(animal)
#         except Exception as e:
#             print(e)

# def main():
#     animal = input('Enter animal name to make admin: ')
#     assign_admin_role(animal.capitalize())

# if __name__ == "__main__":
#     main()