from flask import Flask, request, render_template
import os
from flask_sqlalchemy import SQLAlchemy
from . import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['DATABASE'] = os.path.join(os.getcwd(), 'flask.sqlite')
db.init_app(app)
app.secret_key = 'development key'
db = SQLAlchemy(app)

def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

db_init(app)

from app import routes