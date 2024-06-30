import os

# uri = os.getenv("DATABASE_URL")
# print("URI is ", uri)

class Config:

    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'

    uri = os.getenv("DATABASE_URL")
    if uri:
        if uri.startswith("postgres://"):     
            uri = uri.replace("postgres://", "postgresql://", 1)

    # SQLALCHEMY_DATABASE_URI = uri
    # SECRET_KEY = os.environ.get('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SECRET_KEY = os.environ.get('SECRET_KEY')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'data.shantanu@gmail.com'
    MAIL_PASSWORD = 'PE5bU0mYYi5n1!k'
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
