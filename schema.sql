CREATE TABLE users (id integer, username text, password text, role integer);

CREATE TABLE abbrevations (id integer, abbrevation text, explanation text);

CREATE TABLE literature (id integer, title character varying, author character varying, keywords ARRAY, rating integer, availability character varying);

CREATE TABLE stakeholders (id integer, name text, type text, description text, contact text);
