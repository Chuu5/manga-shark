import json
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
# from flask_session import Session

# Configure application
app = Flask(__name__)

# Configure Database
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Mangas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    banner = db.Column(db.String(120), unique=True, nullable=False)
    summary = db.Column(db.String(120), nullable=False)

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)
    manga_id = db.Column(db.Integer, nullable=False)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        summary = request.form.get("summary")
        name = request.form.get("name").lower()
        banner = request.form.get("banner")

        if not name or not summary or not banner:
            flash("Please fill all Inputs")
            return redirect("/")
        
        mangas = Mangas.query.all()

        for manga in mangas:
            if name in manga.name:
                flash("Manga Already Added")
                return redirect("/")

        manga = Mangas(
            name=name,
            banner=banner,
            summary=summary,
        )
        db.session.add(manga)
        db.session.commit()

        flash("Added!")
        return redirect("/")

    return render_template("index.html",)

@app.route("/mangas", methods=["GET", "POST"])
def mangas():
    mangas = Mangas.query.all()
    if request.method == "POST":
        name = request.form.get("name")
        comment = request.form.get("comment")
        # render one specific manga
        manga = Mangas.query.filter_by(name=name).first()

        manga_id = manga.id
        # if user typed a comment, add new comment to the database
        if comment:
            newComment = Comments(
                text=comment,
                manga_id=manga_id
            )
            db.session.add(newComment)
            db.session.commit()

        comments = Comments.query.filter_by(manga_id=manga.id)

        return render_template("manga.html", manga=manga, comments=comments)

    return render_template("mangas.html", mangas=mangas)


# Thought of making a about page
# @app.route("/about", methods=["GET", "POST"])
# def about():
#     return render_template("about.html")