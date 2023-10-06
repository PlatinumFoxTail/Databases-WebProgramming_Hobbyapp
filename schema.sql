CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, role INTEGER);

CREATE TABLE abbrevations (id SERIAL PRIMARY KEY, abbrevation TEXT, explanation TEXT)

CREATE TABLE literature (id SERIAL PRIMARY KEY, title TEXT, author TEXT, keywords TEXT, rating INTEGER, availability TEXT);

CREATE TABLE stakeholders (id SERIAL PRIMARY KEY, name TEXT, type TEXT, description TEXT, contact TEXT);
