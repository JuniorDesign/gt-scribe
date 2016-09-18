# Notetaking App for GaTech Disability Services

Application written for Fall 2016 Junior Design part 2.

Authors: Sara Cagle, Hosna Chaudhry, Sneh Munshi, Jessica Rosenfield, Brad Ware

## How to turn run this locally:

1. Download the project and navigate to the top level folder.
2. Ensure you have Python here [https://www.python.org/downloads/]
3. Ensure you have Flask `pip install Flask` and flask_restful, `pip install flask_restful` (and anything else it asks you to install.)
4. run `python serve.py`
5. If it prompts you about accepting any incoming connections, be sure to allow it.
6. In your browser, navigate to `localhost:5000` to see the index.html page.

**If you are using Python 3, you will instead use `pip3` instead of `pip` and `python3` instead of `python`.

The content here is still changing.

## Sprint 1:

- Set up initial local server (Flask)
- Set up SQL server
- Create mock login system (just a single button that says 'login')
- Landing page (that has the login button)
- Create admin portal
- Create notetaker portal
- Create noterequester portal
- Registration page for users who haven't signed up formally yet?
- Role picker for testing purposes (notetaker, admin, note requester)
- Investigate CAS



## Sprint 2:

- Feedback page
- Matching of notetakers and requesters
- How to query courses for a specific user


## Sprint 3:

- Implement CAS for official login
- tbd

##Requirements (not case sensitive):

- flask (pip)
- flask_restful (pip)
- flask-SQLAlchemy (pip)
- http://sqlitebrowser.org/ (used to view the current state of db)

