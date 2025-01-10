# Hobby app

This app is related to the field of brain-computer interface, hereafter reffered to as BCI. 

The features of the app are:

- The user can sign in and out and create user name and password and choose role as regular user or admin
- The users can search for meaning of some common BCI related abbrevations e.g. BMI = brain-machine interface
- The users can search and add information of BCI stakeholders e.g. Stakeholder group = Company, Stakholder name = Neuralink, Stakeholder description = Developing implantable brain-computer devices, Stakeholder contact = https://neuralink.com/
- The users can search and add BCI literature e.g. Title, Author, Pre-defined keywords, Rating, Availability
- The users can search and add BCI events e.g. Name, Description, Country, Time, Info.
- The admin can additonally remove BCI abbrevations, stakeholders, literature, events and users

# How to run the app
*Prerequisite*: A PostgreSQL instance running.

Clone this repository to you own computer and navigate to its root folder. In the root folder create a .env file with the following variables defined:
* `DATABASE_URL` for the URL of your PostgreSQL database
* `SECRET_KEY` for the secret key of the Flask application

Afterwards in the same folder create a virtual environment and install dependencies:
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```

Define the database schema with following command:
```
psql < schema.sql
```
Alternatively you can also copy paste the schemas one by one from schema.sql into you PostgreSQL interpreter.

Run the application from the same folder where the app is located with:
```
flask run
```
In case of issues when trying to run the app locally, following info might be useful: https://hy-tsoha.github.io/materiaali/aikataulu/#huomio-flyiosta
