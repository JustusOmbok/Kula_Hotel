from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
app.secret_key = '34293560'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotel.db'

db = SQLAlchemy(app)

from app import routes, models
