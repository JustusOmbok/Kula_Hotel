from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '34293560'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

db = SQLAlchemy(app)

from app import routes, models
