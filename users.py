from db import db
from flask import session 
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

# function for creating a new user to users table
def create_user(username: str, password: str, role: int):
    # hashing password 
    hash_value = generate_password_hash(password)
    
    #inserting username, hash value, and role to users table
    try:
        sql = text("INSERT INTO users (username, password, role) VALUES (:username, :password, :role)")
        db.session.execute(sql, {"username":username, "password":hash_value, "role": role})
        db.session.commit()
    except:
        return False
    
    return login(username, password)

def login(username: str, password: str): 
    # fetching user from database
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False 
    
    stored_hash = user.password
    if not check_password_hash(stored_hash,password):
        return False 
    
    #password correct, sign in can proceed
    session["username"] = username
    
    #adding random csrf_token to decrease csrf vulnerabilities
    session["csrf_token"] = secrets.token_hex(16)

    return True 

def user_exists(username: str): 
        sql = text("SELECT username from users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        existing_user = result.fetchone()

        if existing_user: 
             return True 
        else: 
             return False 

def check_role(username:str):
    query = text(f"SELECT role FROM users WHERE username = :username")
    userrole = db.session.execute(query, {"username": username}).scalar()

    return userrole