from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
#setting environment variable (Osa 2: Ympäristömuuttujat)
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

#setting environment variable (Osa 2: Ympäristömuuttujat)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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


#@app.route("/abbrevations")
#def abbrevations():
    #return "WIP BCI abbrevations"

@app.route("/stakeholders")
def stakeholders():
    return "WIP BCI stakeholders"

@app.route("/literature")
def literature():
    return "WIP BCI literature"

@app.route("/discussions")
def discussions():
    return "WIP BCI discussions"