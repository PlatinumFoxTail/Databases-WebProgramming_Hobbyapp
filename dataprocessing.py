from db import db
from sqlalchemy.sql import text        


def search_abbrevation(abbreviation: str):
    result = db.session.execute(
            text("SELECT explanation FROM abbrevations WHERE abbrevation = :abbreviation"),
            {"abbreviation": abbreviation}
        )
    return result.fetchone()

def add_stakeholder(name:str, type:str, description:str, contact:str):
    #inserting the new stakeholder item into the database
    db.session.execute(
        text("INSERT INTO stakeholders (name, type, description, contact) VALUES (:name, :type, :description, :contact)"),
        {"name": name, "type": type, "description": description, "contact": contact}
    )
    db.session.commit()

    return True

def search_stakeholders(name:str, type:str, description:str, contact:str):
    #building the SQL query based on the provided fields
    query = "SELECT * FROM stakeholders WHERE 1=1"
    params = {}

    if name:
        query += " AND lower(name) LIKE LOWER(:name)"
        params["name"] = f"%{name.lower()}%"
    if type:
        query += " AND LOWER(type) LIKE LOWER(:type)"
        params["type"] = f"%{type.lower()}%"
    if description:
        query += " AND LOWER(description) LIKE LOWER(:description)"
        params["description"] = f"%{description.lower()}%"
    if contact:
        query += " AND LOWER(contact) LIKE LOWER(:contact)"
        params["contact"] = f"%{contact.lower()}%"

    #executing the SQL query
    result = db.session.execute(text(query), params)
    results = result.fetchall()

    return results

def add_literature(title, author, keywords, rating, availability):
    #inserting the new literature item into the database
    db.session.execute(
        text("INSERT INTO literature (title, author, keywords, rating, availability) VALUES (:title, :author, :keywords, :rating, :availability)"),
        {"title": title, "author": author, "keywords": keywords, "rating": rating, "availability": availability}
    )
    db.session.commit()

    return True

def search_literature(title:str, author:str, keywords:str, rating:int, availability:str):

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

    return results

def add_event(name, description, country, time, info):
    #inserting the new event item into the database
    db.session.execute(
        text("INSERT INTO events (name, description, country, time, info) VALUES (:name, :description, :country, :time, :info)"),
        {"name": name, "description": description, "country": country, "time": time, "info": info}
    )
    db.session.commit()

    return True

def search_events(name, description, country, time, info):
    #building the SQL query based on the provided fields
    query = "SELECT * FROM events WHERE 1=1"
    params = {}

    if name:
        query += " AND lower(name) LIKE LOWER(:name)"
        params["name"] = f"%{name.lower()}%"
    if description:
        query += " AND LOWER(description) LIKE LOWER(:description)"
        params["description"] = f"%{description.lower()}%"
    if country:
        query += " AND LOWER(country) LIKE LOWER(:country)"
        params["country"] = f"%{country.lower()}%"
    if time:
        if len(time) == 4:  # Input in YYYY format
            query += " AND EXTRACT(YEAR FROM time) = :year"
            params["year"] = int(time)
        elif len(time) == 7:  # Input in YYYY-MM format 
            query += " AND EXTRACT(YEAR FROM time) = :year AND EXTRACT(MONTH FROM time) = :month"
            year, month = map(int, time.split("-"))
            params["year"] = year
            params["month"] = month
        elif len(time) == 10:  # Input in YYYY-MM-DD format
            query += " AND time = :time"
            params["time"] = time
        else:
            # Handle invalid input here, if necessary
            pass

    if info:
        query += " AND LOWER(info) LIKE LOWER(:info)"
        params["info"] = f"%{info.lower()}%"

    #executing the SQL query
    result = db.session.execute(text(query), params)
    results = result.fetchall()

    return results

def remove_row(table_name, row_id):
    #trying to remove selected row from selected table, else False
    try:
        query0 = text(f"DELETE FROM {table_name} WHERE id = :row_id")
        params = {"row_id": row_id}
        db.session.execute(query0, params)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()
        return False

def fetch_literature():
    query1 = "SELECT * FROM literature WHERE 1=1"
    result1 = db.session.execute(text(query1))
    literature = result1.fetchall()

    return literature

def fetch_abbrevations():
    query2 = "SELECT * FROM abbrevations WHERE 1=1"
    result2 = db.session.execute(text(query2))
    abbrevations = result2.fetchall()

    return abbrevations

def fetch_stakeholders():
    query3 = "SELECT * FROM stakeholders WHERE 1=1"
    result3 = db.session.execute(text(query3))
    stakeholders = result3.fetchall()

    return stakeholders

def fetch_users():
    query4 = "SELECT id, username, role FROM users WHERE 1=1;"
    result4 = db.session.execute(text(query4))
    users = result4.fetchall()

    return users

def fetch_events():
    query5 = "SELECT id, name, description, country, time, info FROM events WHERE 1=1;"
    result5 = db.session.execute(text(query5))
    events = result5.fetchall()

    return events