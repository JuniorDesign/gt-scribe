# GT Scribe, the Notetaker Registration App for the Georgia Tech Disability Services

Application written for Fall 2016 Junior Design part 2.

Authors: Sara Cagle, Hosna Chaudhry, Sneh Munshi, Jessica Rosenfield, Brad Ware

**This application requires Python3 to run locally. You cannot use Python 2.**

## How to turn run this locally:

1. Download the project and navigate to the top level folder.
2. Ensure you have Python3 [here](https://www.python.org/downloads/) It can be downloaded directly from the website.
3. Ensure you have Flask; you can use Pip3 to install it. `p3ip install Flask` and flask_restful, `pip3 install flask_restful`, `pip3 install flask-SQLAlchemy`, `pip3 install boto3` (and anything else it asks you to install.)
4. Create the database before running this for the first time. Do this with: `python3 manage.py create_db`, `python3 manage.py populate_courses`, `python3 manage.py populate_users`. If there are any errors in this process, drop the db and then restart this step, `python3 manage.py drop_db`.
5. Run `python3 serve.py`
6. If it prompts you about accepting any incoming connections, be sure to allow it.
7. In your Internet browser, navigate to `localhost:5000` to see the rendered index page.
8. For working with the database, we recommend you download DB Browser for SQLite, which can be found [here](http://sqlitebrowser.org/). In the SQLite Browser, open the database (`temp.db`, inside the `data` folder) to view and directly edit its contents. Be sure to select "Write Changes" to save changes. If the script does not work, try manually making the `data` folder first, then running the script

**This readme is dynamic and frequently undergoes changes.**

## Sprint 1:

- Set up initial local server (Flask)
- Set up SQLite database
- Landing page with "login" and "register user" options
- Create register user page
- Create user login page (or functionality on the landing page)
- Role picker for testing purposes (notetaker, admin, note requester)
- Connect the register page to post data to the db
- Connect the login page to cross reference data from the db
- Create admin portal
- Create notetaker portal
- Create noterequester portal
- Investigate CAS



## Sprint 2:

- Feedback page
- Matching of notetakers and requesters
- Create schema for GaTech courses
- Define the relationships of students and their courses
- tbd


## Sprint 3:

- Implement CAS for official login(?)
- tbd
