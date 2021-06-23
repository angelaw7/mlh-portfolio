from flask import render_template, request
from app import app, db
from app.models import Blog
import os
import smtplib
from app.websiteData import *


# Routes
@app.route('/')
def index():
    return render_template('about.html', title="MLH Fellow", url=os.getenv("URL"), headerInfo=headerInfo, aboutInfo=aboutInfo)

@app.route('/about')
def aboutMe():
    return render_template('about.html', headerInfo=headerInfo, aboutInfo=aboutInfo)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html', headerInfo=headerInfo, projects=projects)

@app.route('/blog')
def blogPage():
    blog_posts = get_posts()
    path = 'app/static/img/blog/'
    for post in blog_posts:
        post.content = post.content[:255] + '...'
        with open(path + post.img_name, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(post.img)
    return render_template('blog.html', url=os.getenv("URL"), headerInfo=headerInfo, blog_posts=blog_posts)

# New blog post page
@app.route('/new-blog')
def new_blog():
    return render_template('new_blog.html', title="New Blog", url=os.getenv("URL"), projects=projects)

# View full details about a blog
@app.route('/blog/<int:id>')
def get_post(id):
    post = Blog.query.filter_by(id=id).first()
    if not post:
        return 'Post Not Found!', 404

    return render_template('detail_blog.html', url=os.getenv("URL"), title=post.title, post=post)

@app.route('/contact')
def contact():
    return render_template('contact.html', url=os.getenv("URL"), headerInfo=headerInfo)

@app.route('/health')
def healthy():
    db.engine.execute('SELECT 1')
    return ''

# Send email through contact page
@app.route('/sendMsg', methods=['POST'])
def sendMsg():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    if not name or not email or not message:
        return 'Not enough data!', 400

    message2Send = '\nName: ' + name + ' \nEmail: ' + email + '\nMessage: ' + message
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('lightshield539@gmail.com', 'bOTspam21')
    server.sendmail('testmlh.pod.333@gmail.com', 'wangela472@gmail.com', message2Send)
    return render_template('success.html', url=os.getenv("URL"), headerInfo=headerInfo)

# Create new blog post
@app.route('/upload', methods=['POST'])
def upload():
    pic = request.files['pic']
    title = request.form['name']
    content = request.form['blog-content']

    if not pic or not title or not content:
        return 'Not enough data!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Not enough data!', 400

    post = Blog(title=title, content=content, img=pic.read(), img_name=filename, img_mimetype=mimetype)
    db.session.add(post)
    db.session.commit()

    return render_template('success.html', url=os.getenv("URL"), headerInfo=headerInfo)

def get_posts():
    posts = Blog.query.order_by(Blog.date_created).all()
    return posts