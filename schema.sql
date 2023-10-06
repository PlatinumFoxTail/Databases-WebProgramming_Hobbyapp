CREATE TABLE users (id integer, username text, password text, role integer);

CREATE TABLE abbrevations (id integer, abbrevation text, explanation text);

CREATE TABLE literature (id SERIAL PRIMARY KEY, title TEXT, author TEXT, keywords TEXT, rating INTEGER, availability TEXT);

CREATE TABLE stakeholders (id integer, name text, type text, description text, contact text);
