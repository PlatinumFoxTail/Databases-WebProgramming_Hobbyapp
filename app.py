from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2:///habmarti?host=/home/habmarti/pgsql/sock"
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/abbrevations")
def abbrevations():
    return "WIP BCI abbrevations"

@app.route("/stakeholders")
def stakeholders():
    return "WIP BCI stakeholders"

@app.route("/literature")
def literature():
    return "WIP BCI literature"

@app.route("/discussions")
def discussions():
    return "WIP BCI discussions"