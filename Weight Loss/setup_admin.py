from flaskapp import create_app, db
from flaskapp.models import User

app = create_app()

def assign_admin_role(animal):
    with app.app_context():
        db.init_app(app)
        try:
            User.create_admin(animal)
        except Exception as e:
            print(e)

def main():
    animal = input('Enter animal name to make admin: ')
    assign_admin_role(animal.capitalize())

if __name__ == "__main__":
    main()