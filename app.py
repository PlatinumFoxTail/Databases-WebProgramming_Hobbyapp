from flask import Flask, render_template, request, flash, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def create_user():

    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form ["password2"]
        role = int(request.form["role"])
        
        #checking if username taken
        sql = text("SELECT username from users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        existing_user = result.fetchone()
        if existing_user is not None:
            return render_template("error.html", message="Choose another username.")
        
        #checking if Password and Repeated password same
        if password1 != password2:
            return render_template("error.html", message="Entered passwords do not match")

        # Hahmotellaan salasanan hajautusarvo ja tallennetaan se tietokantaan
        hash_value = generate_password_hash(password1)
        sql = text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)")
        db.session.execute(sql, {"username":username, "password":hash_value, "role": role})
        db.session.commit()
        
        flash("User created", "success")
        return redirect("/register")
    
    return render_template("register.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    # adding random csrf_token to decrease csrf vulnerabilities
    session["csrf_token"] = secrets.token_hex(16)

    # Haetaan käyttäjä tietokannasta
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        # Käyttäjää ei löytynyt, voit lisätä tähän sopivan virheilmoituksen
        return "Invalid username"

    stored_hash = user.password

    if check_password_hash(stored_hash, password):
        # Salasana on oikein, voit suorittaa kirjautumisen
        session["username"] = username
        return redirect("/welcome")
    else:
        # Väärä salasana, voit lisätä tähän sopivan virheilmoituksen
        return "Invalid password"

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

@app.route("/abbrevations", methods=["GET", "POST"])
def abbrevations():

    abbreviation = None
    explanation = None

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        # Retrieve the abbreviation entered by the user
        abbreviation = request.form.get("abbreviation")

        # Query the database for the explanation
        result = db.session.execute(
            text("SELECT explanation FROM abbrevations WHERE abbrevation = :abbreviation"),
            {"abbreviation": abbreviation}
        )
        explanation = result.fetchone()

    return render_template("abbrevations.html", abbreviation=abbreviation, explanation=explanation)

#Adding stakeholder into stakeholder table
@app.route("/stakeholders", methods=["GET", "POST"])
def stakeholders():
    name = None
    type = None
    description = None
    contact = None
    results = None  

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if "name" in request.form and "type" in request.form and "description" in request.form and "contact" in request.form:
            #handling the form submission for adding a new literature item
            name = request.form.get("name")
            type = request.form.get("type")
            description = request.form.get("description")
            contact = request.form.get("contact")

            #inserting the new stakeholder item into the database
            db.session.execute(
                text("INSERT INTO stakeholders (name, type, description, contact) VALUES (:name, :type, :description, :contact)"),
                {"name": name, "type": type, "description": description, "contact": contact}
            )
            db.session.commit()
            flash("Stakeholder item added successfully", "success")

            # Redirect to the same route after adding
            return redirect(url_for("stakeholders"))

    #if the request method is "GET," return a response here (e.g., render a template or redirect)
    return render_template("stakeholders.html", name=name, type=type, description=description, contact=contact, results=results)

#searching stakeholder
@app.route("/searchstakeholders", methods=["POST"])
def searchstakeholders():
    name = None
    type = None
    description = None
    contact = None
    results = None
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if "name" in request.form or "type" in request.form or "description" in request.form or "contact" in request.form:
            #handling the form submission for adding a new literature item
            name = request.form.get("name")
            type = request.form.get("type")
            description = request.form.get("description")
            contact = request.form.get("contact")
            
            #building the SQL query based on the provided fields
            query = "SELECT * FROM stakeholders WHERE 1=1"
            params = {}

            if name:
                query += " AND name = :name"
                params["name"] = name
            if type:
                query += " AND type = :type"
                params["type"] = type
            if description:
                query += " AND description = :description"
                params["description"] = description
            if contact:
                query += " AND contact = :contact"
                params["contact"] = contact

            #executing the SQL query
            result = db.session.execute(text(query), params)
            results = result.fetchall()
    
    #return the template with results
    return render_template("stakeholders.html", name=name, type=type, description=description, contact=contact, results=results)

#Adding literature into literature table
@app.route("/literature", methods=["GET", "POST"])
def literature():
    title = None
    author = None
    keywords = None
    rating = None
    availability = None
    results = None  

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if "title" in request.form and "author" in request.form and "keywords" in request.form and "rating" in request.form and "availability" in request.form:
            #handling the form submission for adding a new literature item
            title = request.form.get("title")
            author = request.form.get("author")
            keywords = request.form.get("keywords")
            rating = request.form.get("rating")
            availability = request.form.get("availability")

            #inserting the new literature item into the database
            db.session.execute(
                text("INSERT INTO literature (title, author, keywords, rating, availability) VALUES (:title, :author, :keywords, :rating, :availability)"),
                {"title": title, "author": author, "keywords": keywords, "rating": rating, "availability": availability}
            )
            db.session.commit()
            flash("Literature item added successfully", "success")

            # Redirect to the same route after adding
            return redirect(url_for("literature"))

    #if the request method is "GET," return a response here (e.g., render a template or redirect)
    return render_template("literature.html", title=title, author=author, keywords=keywords, rating=rating, availability=availability, results=results)

#searching literature
@app.route("/searchbooks", methods=["POST"])
def searchbooks():
    title = None
    author = None
    keywords = None
    rating = None
    availability = None
    results = None
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if "title" in request.form or "author" in request.form or "keywords" in request.form or "rating" in request.form or "availability" in request.form:
            title = request.form.get("title")
            author = request.form.get("author")
            keywords = request.form.get("keywords")
            rating = request.form.get("rating")
            availability = request.form.get("availability")
            
            #building the SQL query based on the provided fields
            query = "SELECT * FROM literature WHERE 1=1"
            params = {}

            if title:
                query += " AND LOWER(title) LIKE LOWER(:title)"
                params["title"] = f"%{title.lower()}%"
            if author:
                query += " AND LOWER(author) LIKE LOWER(:author)"
                params["author"] = f"%{author.lower()}%"
            if keywords:
                query += " AND LOWER(keywords) LIKE LOWER(:keywords)"
                params["keywords"] = f"%{keywords.lower()}%"
            if rating:
                query += " AND rating = :rating"
                params["rating"] = rating
            if availability:
                query += " AND LOWER(availability) LIKE LOWER(:availability)"
                params["availability"] = f"%{availability.lower()}%"

            #executing the SQL query
            result = db.session.execute(text(query), params)
            results = result.fetchall()
    
    #return the template with results
    return render_template("literature.html", title=title, author=author, keywords=keywords, rating=rating, availability=availability, results=results)

@app.route('/admin', methods=["GET", "POST"])
def admin():
    username = session.get('username')
    query = text(f"SELECT role FROM users WHERE username = :username")
    userrole = db.session.execute(query, {"username": username}).scalar()

    if userrole == 1:
        flash("No admin rights to enter Admin page", "success")
        return render_template("welcome.html")
    
    #If the user is an admin, then proceeding to admin.html

    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        table_name = request.form.get("table")
        row_id = request.form.get("id")

        query0 = text(f"DELETE FROM {table_name} WHERE id = :row_id")
        params = {"row_id": row_id}
        db.session.execute(query0, params)
        db.session.commit()

        flash(f"Row with id = {row_id} removed succesfully from table {table_name}", "success")



    query1 = "SELECT * FROM literature WHERE 1=1"
    result1 = db.session.execute(text(query1))
    literature = result1.fetchall()


    query2 = "SELECT * FROM abbrevations WHERE 1=1"
    result2 = db.session.execute(text(query2))
    abbrevations = result2.fetchall()

    query3 = "SELECT * FROM stakeholders WHERE 1=1"
    result3 = db.session.execute(text(query3))
    stakeholders = result3.fetchall()

    query4 = "SELECT id, username, role FROM users WHERE 1=1;"
    result4 = db.session.execute(text(query4))
    users = result4.fetchall()
    
    return render_template("admin.html", abbrevations=abbrevations, literature=literature, stakeholders=stakeholders, users=users)