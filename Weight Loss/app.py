from flaskapp import create_app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)