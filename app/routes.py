from flask import render_template, request
from app import app, db
from app.models import Blog
import os
import smtplib

headerInfo = {
    'img':'./static/img/fbcoverimg.jpg',
    'name': 'Angela Wang',
    'intro': 'Software and Biomedical Engineering Student, MLH Fellow'
}

aboutInfo = {
    'shortParagraph': "Hey! My name is Angela and I'm a Software and Biomedical Engineering student at McMaster University. I'm passionate about medicine and technology and I hope to integrate both fields to one day work on developing innovative medical devices. I love to learn new things and I will never turn down an opportunity to continue developing my skills and exploring my interests. I'm currently participating in the Production Engineering Track of the MLH Fellowship this summer, where I'm learning  about Production/Site Reliability Engineering and DevOps. I'm also exploring Full-stack Development and I've recently taken an interest in Computer Vision and Machine Learning. \nIf anything here piques your interests, feel free to reach out! I'd love to connect and have a chat.",
    'education': [
        {
            'schoolName': 'McMaster University',
            'year': '2020 - 2025',
            'description':'McMaster Developers Students Club, McMaster Start Coding, Medical Makers'
        }
    ],
    'interest': ['Interest 1', 'Interest 2', 'Interest 3'],
    'experience': [
        {
            'jobTitle': 'MLH Production Engineering Fellow',
            'year': 'June 2021 - August 2021',
            'jobDesc': 'Production Engineering, also known as Site Reliability Engineering & DevOps, is a hybrid between software & systems engineering that works across product & infrastructure to make sure services are reliable & scalable.'
        },
        {
            'jobTitle': 'Makria Web Developer',
            'year': 'June 2021 - August 2021',
            'jobDesc': 'Updating and revising the Makria website using Wordpress. Managing plugings, Javascript interactions, eCommerce integrations.'
        }
    ],
    'skill': [
        {'name':'Python', 'icon':'fab fa-python'},
        {'name':'Javascript','icon':'fab fa-js-square'},
        {'name':'HTML/CSS','icon':'fab fa-html5'}
        ]
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

@app.route('/contact')
def contact():
    return render_template('contact.html', url=os.getenv("URL"), headerInfo=headerInfo)


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
        return 'Not enough data!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Not enough data!', 400

    post = Blog(title=title, content=content, img=pic.read(), img_name=filename, img_mimetype=mimetype)
    db.session.add(post)
    db.session.commit()

    return render_template('success.html', url=os.getenv("URL"), headerInfo=headerInfo)


@app.route('/blog/<int:id>')
def get_post(id):
    post = Blog.query.filter_by(id=id).first()
    if not post:
        return 'Post Not Found!', 404

    return render_template('detail_blog.html', url=os.getenv("URL"), title=post.title, post=post)


def get_posts():
    posts = Blog.query.order_by(Blog.date_created).all()
    return posts

@app.route('/health')
def healthy():
    db.engine.execute('SELECT 1')
    return ''