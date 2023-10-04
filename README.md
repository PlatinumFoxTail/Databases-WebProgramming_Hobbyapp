# BCI's LITTLE HELPER APP

This app is related to the field of brain-computer interface, hereafter reffered to as BCI. 

The features of the app are:

- The user can sign in and out and create user name and password and choose role as regular user or admin
- The users can search for meaning of some common BCI related abbrevations e.g. BMI = brain-machine interface
- The users can search and add information of BCI stakeholders e.g. Stakeholder group = Company, Stakholder name = Neuralink, Stakeholder description = Developing implantable brain-computer devices, Stakeholder contact = https://neuralink.com/
- The users can search and add BCI literature e.g. Title, Author, Pre-defined keywords, Rating, Availability
- The admin can additonally remove BCI abbrevations, stakeholders, literature, and users

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

## Status at Intermediate hand-in 24.9.23:

I. General status of app:
- Search abbrevations OK.
- Search and add literature OK. NB! The keywords section should be added within {}
- Search and add stakeholders OK.
- Register and login OK.
- Admin can remove data OK.

II. Literature page improvement needs:
- The accepted form of BCI literature search should be dipslayed in the search boxes in gray e.g. keywords as {keyword1, keyword2}
- Some type of message should be displayed if Add literature is succesful or unsucessful or already added
- Title size of BCI literature search as h2 and h1 as Literature search
- Consider if have time to fine tune search function that can only add parts of the search items e.g. Brain computer*, only one keyword

III. Stakeholder  page improvement needs:
- The accepted form of BCI stakeholder search should be dipslayed in the search boxes in gray
- Some type of message should be displayed if Add stakeholder is succesful or unsucessful or already added
- Title size of BCI literature search changed to BCI stakeholder search and title as h2 and h1 as Add BCI stakeholder 
- Consider if have time to fine tune search function that can only add parts of the search items e.g. Device* in description
- Make the box larger so can see options for type searches

IV. Project scope revision
- It was noticed and decided togther with course assistant, that the original planned BCI discussion feature was too extensive to include into the project. So following feature was decided to leave out from the project:

"The user can search and add comments to BCI related discussions e.g. Discussion topic: "BCI job openings in Finland" -> User1: "Can not find BCI companies in Finland. Any suggestions of companies based in Finland adjacent to BCI field?" -> User2: "You can try reaching out to comapny x, y, and z" -> User1: "I reached out to them both, and actually company y is about to initiate something in the field, so I will add it into the BCI stakeholder list""
