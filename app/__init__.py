from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.secret_key = 'development key'
db = SQLAlchemy(app)

def db_init(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()

db_init(app)

from app import routes