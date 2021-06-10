import os
from flask import Flask, request, Response, render_template, send_file, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from db import db_init, db
from models import Blog
from contactForm import ContactForm



load_dotenv()
app = Flask(__name__)
 
app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db_init(app)

headerInfo = {
    'img':'./static/img/coverimg.jpg',
    'name': 'Fellow Name',
    'intro': 'Short intro here'
}

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


# Pages
@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"), headerInfo=headerInfo, projects=projects)


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', headerInfo=headerInfo, projects=projects)


@app.route('/blog')
def blogPage():
    blog_posts = get_posts()
    for post in blog_posts:
        post.img = send_file(post.img, post.img_mimetype)
    return render_template('blog.html', url=os.getenv("URL"), headerInfo=headerInfo, blog_posts=blog_posts)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    return render_template('contact.html', headerInfo=headerInfo, form=form)


# Creating new blog posts
@app.route('/new-blog')
def new_blog():
    return render_template('new_blog.html', title="New Blog", url=os.getenv("URL"), projects=projects)


@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    title = request.form['name']
    content = request.form['blog-content']

    if not pic or not title or not content:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    post = Blog(title=title, content=content, img=pic.read(), img_name=filename, img_mimetype=mimetype)
    db.session.add(post)
    db.session.commit()

    return 'Post Uploaded', 200


@app.route('/blog/<int:id>')
def get_post(id):
    post = Blog.query.filter_by(id=id).first()
    if not post:
        return 'Img Not Found!', 404

    return Response(post.img, mimetype=post.img_mimetype)


def get_posts():
    posts = Blog.query.order_by(Blog.date_created).all()
    return posts
