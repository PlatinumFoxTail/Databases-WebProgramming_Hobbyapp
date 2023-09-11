from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Welcome to BCI's little helper"

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