from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from sqlalchemy import or_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"  # Flask's session management requires a secret key to be set for security reasons. Needed at least for adding literature in literature page.
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/abbrevations", methods=["GET", "POST"])
def abbrevations():
    abbreviation = None
    explanation = None

    if request.method == "POST":
        # Retrieve the abbreviation entered by the user
        abbreviation = request.form.get("abbreviation")

        # Query the database for the explanation
        result = db.session.execute(
            text("SELECT explanation FROM abbrevations WHERE abbrevation = :abbreviation"),
            {"abbreviation": abbreviation}
        )
        explanation = result.fetchone()

    return render_template("abbrevations.html", abbreviation=abbreviation, explanation=explanation)

@app.route("/stakeholders")
def stakeholders():
    return "WIP BCI stakeholders"

@app.route("/literature", methods=["GET", "POST"])
def literature():
    if request.method == "POST":
        # Handle the form submission for adding a new literature item
        title = request.form.get("title")
        author = request.form.get("author")
        keywords = request.form.get("keywords")
        rating = request.form.get("rating")
        availability = request.form.get("availability")

        # Insert the new literature item into the database
        db.session.execute(
            text("INSERT INTO literature (title, author, keywords, rating, availability) VALUES (:title, :author, :keywords, :rating, :availability)"),
            {"title": title, "author": author, "keywords": keywords, "rating": rating, "availability": availability}
        )
        db.session.commit()
        flash("Literature item added successfully", "success")

        return redirect(url_for("literature"))
    return render_template("literature.html")


    #title = request.form.get("title")
    #author = request.form.get("author")
    #keywords = request.form.get("keywords")
    #rating = request.form.get("rating")
    #availability = request.form.get("availability")

    ## Build the SQL query dynamically based on the provided fields
    #query = "SELECT * FROM literature WHERE 1=1"
    #params = {}

    #if title:
        #query += " AND title = :title"
        #params["title"] = title
    #if author:
        #query += " AND author = :author"
        #params["author"] = author
    #if keywords:
        #query += " AND keywords = :keywords"
        #params["keywords"] = keywords
    #if rating:
        #query += " AND rating = :rating"
        #params["rating"] = rating
    #if availability:
        #query += " AND availability = :availability"
        #params["availability"] = availability

    ## Execute the SQL query
    #result = db.session.execute(text(query), params)
    #results = result.fetchall()

    #return render_template("literature.html", title=title, author=author, keywords=keywords, rating=rating, availability=availability, results=results)

@app.route("/discussions")
def discussions():
    return "WIP BCI discussions"