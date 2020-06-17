import os

from main import app

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://postgres:suriniva1107@localhost/cf"
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "secret key"
