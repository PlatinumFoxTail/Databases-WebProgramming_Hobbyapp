from app import app
from flask import render_template, request, flash, redirect, url_for, session, abort
import dataprocessing
import users

@app.route("/")
def index():
    return render_template("index.html")

# creating user
@app.route("/register", methods=["GET", "POST"])
def create_user():

    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form ["password2"]
        role = int(request.form["role"]) 

        #checking if Password and Repeated password same
        if password1 != password2:
            return render_template("error.html", message="Entered passwords do not match")
        
        #checking if username taken
        if users.user_exists(username) == True: 
            return render_template("error.html", message="Choose another username.")
        
        #adding new user to users table
        users.create_user(username, password1, role) 
    
        flash("User created", "success")
        return redirect("/register")
    
    return render_template("register.html")

# logging in
@app.route("/login",methods=["GET", "POST"]) 
def login():
    if request.method == "GET": 
        return render_template("welcome.html") 
    
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]

    if not users.login(username, password): 
        return render_template("error.html", message="Check username or password") 
   
    return redirect("/welcome")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")

# searching abbrevation
@app.route("/abbrevations", methods=["GET", "POST"])
def abbrevations():

    abbreviation = None
    explanation = None

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        # Retrieve the abbreviation entered by the user
        abbreviation = request.form.get("abbreviation")

        # Retrive the corresponding explanation to the entered abbrevation
        explanation = dataprocessing.search_abbrevation(abbreviation)

        if not explanation:
            flash(f"No matches found for {abbreviation}", "success")

    return render_template("abbrevations.html", abbreviation=abbreviation, explanation=explanation)

# adding stakeholder
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
            #handling the form submission for adding a new stakeholder item
            name = request.form.get("name")
            type = request.form.get("type")
            description = request.form.get("description")
            contact = request.form.get("contact")
            
            # checking if the stakeholder already added
            check = dataprocessing.search_stakeholders(name, type, description, contact)

            # if stakeholder not already added, adding stakeholder
            if not check:
                dataprocessing.add_stakeholder(name, type, description, contact)
                flash("Stakeholder item added successfully", "success")
            
            else:
                flash("Stakholder not added, since already in database", "success")

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
            name = request.form.get("name")
            type = request.form.get("type")
            description = request.form.get("description")
            contact = request.form.get("contact")

            results = dataprocessing.search_stakeholders(name, type, description, contact)

            if not results:
                flash(f"No matches found for search", "success")
        
    return render_template("stakeholders.html", name=name, type=type, description=description, contact=contact, results=results)

# adding literature
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

            check = dataprocessing.search_literature(title, author, keywords, rating, availability)
            
            if not check:
                dataprocessing.add_literature(title, author, keywords, rating, availability)
                flash("Literature item added successfully", "success")
            else:
                flash("Literature not added, since already in database", "success")

            # Redirect to the same route after adding
            return redirect(url_for("literature"))

    #if the request method is "GET," return a response here (e.g., render a template or redirect)
    return render_template("literature.html", title=title, author=author, keywords=keywords, rating=rating, availability=availability, results=results)

# searching literature
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
            #handling the form submission for searching literature item
            title = request.form.get("title")
            author = request.form.get("author")
            keywords = request.form.get("keywords")
            rating = request.form.get("rating")
            availability = request.form.get("availability")

            results = dataprocessing.search_literature(title, author, keywords, rating, availability)

            if not results:
                flash(f"No matches found for search", "success")

    #return the template with results
    return render_template("literature.html", title=title, author=author, keywords=keywords, rating=rating, availability=availability, results=results)

# adding event
@app.route("/events", methods=["GET", "POST"])
def events():
    name = None
    description = None
    country = None
    time = None
    info = None
    results = None  

    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if "name" in request.form and "description" in request.form and "country" in request.form and "time" in request.form and "info" in request.form:
            #handling the form submission for adding a new event item
            name = request.form.get("name")
            description = request.form.get("description")
            country = request.form.get("country")
            time = request.form.get("time")
            info = request.form.get("info")
            
            check = dataprocessing.search_events(name, description, country, time, info)

            if not check:
                dataprocessing.add_event(name, description, country, time, info)
                flash("Event item added successfully", "success")
            else:
                flash("Event not added, since already in database", "success")

            # Redirect to the same route after adding
            return redirect(url_for("events"))

    #if the request method is "GET," return a response here (e.g., render a template or redirect)
    return render_template("events.html", name=name, description=description, country=country, time=time, info=info, results=results)

# searching event
@app.route("/searchevents", methods=["POST"])
def searchevents():
    name = None
    description = None
    country = None
    time = None
    info = None
    results = None
    
    if request.method == "POST":
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if "name" in request.form or "description" in request.form or "country" in request.form or "time" in request.form or "info" in request.form:
            #handling the form submission for searching an event item
            name = request.form.get("name")
            description = request.form.get("description")
            country = request.form.get("country")
            time = request.form.get("time")
            info = request.form.get("info")

            results = dataprocessing.search_events(name, description, country, time, info)

            if not results:
                flash(f"No matches found for search", "success")
                
    #return the template with results
    return render_template("events.html", name=name, description=description, country=country, time=time, info=info, results=results)

# admin removal of data
@app.route('/admin', methods=["GET", "POST"])
def admin():
    username = session.get('username')

    userrole = users.check_role(username)

    abbrevations = []
    literature = []
    stakeholders = []
    users_data = []
    events = []

    if userrole == 1:
        flash("No admin rights to enter Admin page", "success")
        return render_template("welcome.html")
    
    #If the user is an admin, then proceeding to admin.html
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        table_name = request.form.get("table")
        row_id = request.form.get("id")

        remove = dataprocessing.remove_row(table_name, row_id)

        if remove == True:
            flash(f"Row with id = {row_id} removed succesfully from table {table_name}", "success")
        if remove == False:
            flash(f"Please try again, row {row_id} not removed from {table_name}", "success")

    abbrevations = dataprocessing.fetch_abbrevations()
    literature = dataprocessing.fetch_literature()
    stakeholders = dataprocessing.fetch_stakeholders()
    users_data = dataprocessing.fetch_users()
    events = dataprocessing.fetch_events()

    return render_template("admin.html", abbrevations=abbrevations, literature=literature, stakeholders=stakeholders, users=users_data, events=events)

        