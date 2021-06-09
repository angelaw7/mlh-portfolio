import os
from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

projects = [
    {
        'title': 'Flask Web App',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eu sapien and lorem fermentum hendrerit quis mattis arcu. Nulla eget efficitur ex. Proin hendrerit ligula quis vehicula interdum.',
        'date': '06/09/2021',
        'img': './static/img/projects/web-dev.jpg',
        'url': 'www.github.com',
    },
    {
        'title': 'Machine Learning Project For Data Prediction',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. In eu sapien and lorem fermentum hendrerit quis mattis arcu. Nulla eget efficitur ex. Proin hendrerit ligula quis vehicula interdum.',
        'date': '06/09/2021',
        'img': './static/img/projects/machine-learning.jpg',
        'url': 'www.github.com',
    },
]

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), projects=projects)
