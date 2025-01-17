from flask import render_template, request
from app import app, db
from app.models import Blog
import os
import smtplib
from app.website_data import about_info, header_info, projects
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# from app.db import get_db


class UserModel(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User {self.username}>"


# Routes
@app.route("/")
def index():
    return render_template(
        "about.html",
        title="MLH Fellow",
        url=os.getenv("URL"),
        header_info=header_info,
        about_info=about_info,
    )


@app.route("/about")
def aboutMe():
    return render_template(
        "about.html", header_info=header_info, about_info=about_info
    )  # noqa: E501


@app.route("/portfolio")
def portfolio():
    return render_template(
        "portfolio.html", header_info=header_info, projects=projects
    )  # noqa: E501


@app.route("/blog")
def blogPage():
    blog_posts = get_posts()
    path = "app/static/img/blog/"
    for post in blog_posts:
        post.content = post.content[:255] + "..."
        with open(path + post.img_name, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(post.img)
    return render_template(
        "blog.html",
        url=os.getenv("URL"),
        header_info=header_info,
        blog_posts=blog_posts,
    )


# New blog post page
@app.route("/new-blog")
def new_blog():
    return render_template(
        "new_blog.html",
        title="New Blog",
        url=os.getenv("URL"),
        projects=projects,  # noqa: E501
    )


# View full details about a blog
@app.route("/blog/<int:id>")
def get_post(id):
    post = Blog.query.filter_by(id=id).first()
    if not post:
        return "Post Not Found!", 404

    return render_template(
        "detail_blog.html", url=os.getenv("URL"), title=post.title, post=post
    )


@app.route("/contact")
def contact():
    return render_template(
        "contact.html", url=os.getenv("URL"), header_info=header_info
    )


@app.route("/health")
def healthy():
    return "Healthy!"


# Send email through contact page
@app.route("/sendMsg", methods=["POST"])
def sendMsg():
    name = request.form["name"]
    email = request.form["email"]
    message = request.form["message"]
    if not name or not email or not message:
        return "Not enough data!", 400

    message2Send = (
        "\nName: " + name + " \nEmail: " + email + "\nMessage: " + message
    )  # noqa: E501
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("testmlh.pod.333@gmail.com", "iampod333")
    server.sendmail(
        "testmlh.pod.333@gmail.com", "wangela472@gmail.com", message2Send
    )  # noqa: E501
    return render_template(
        "success.html", url=os.getenv("URL"), header_info=header_info
    )


# Create new blog post
@app.route("/upload", methods=["POST"])
def upload():
    pic = request.files["pic"]
    title = request.form["name"]
    content = request.form["blog-content"]

    if not pic or not title or not content:
        return "Not enough data!", 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return "Not enough data!", 400

    post = Blog(
        title=title,
        content=content,
        img=pic.read(),
        img_name=filename,
        img_mimetype=mimetype,
    )

    db.session.add(post)
    db.session.commit()

    return render_template(
        "success.html", url=os.getenv("URL"), header_info=header_info
    )


def get_posts():
    posts = Blog.query.order_by(Blog.date_created).all()
    return posts


@app.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif UserModel.query.filter_by(username=username).first() is not None:
            error = "User {username} is already registered."

        if error is None:
            new_user = UserModel(username, generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return "User {username} created successfully"
        else:
            return error, 418

    return render_template(
        "register.html", url=os.getenv("URL"), header_info=header_info
    )


@app.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None
        user = UserModel.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    return render_template(
        "login.html", url=os.getenv("URL"), header_info=header_info
    )  # noqa: E501
