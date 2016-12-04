# GT Scribe, the Notetaker Registration and Matching App

![GT Scribe Logo](http://i68.tinypic.com/6o1pgg.png) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ![Team 94 Logo](http://i68.tinypic.com/10gbsw0.png)


### Inspired by and created with guidance from the Office of Georgia Tech Disability Services

Application written for Fall 2016 Junior Design part 2.

Authors: Sara Cagle, Hosna Chaudhry, Sneh Munshi, Jessica Rosenfield, Brad Ware


## Release notes:

- New software features for this release
- Bug fixes made since the last release

**Known bugs and defects** 

- Routes within the application are not secure to specific users. If a student is logged in, he can navigate to any student views within the app, regardless of his enrolled courses.
- Students who have not been approved by administrators can still be matched and receive notes from/take notes for other students.
- App is not confirmed WCAG 2.0 compliant.
- App is not fully responsive.
- App is not on the cloud and can only be run locally.
- you should also include here any functionality you promised the customer but which is missing in the release

## Installation Guide:

**Pre-requisits**

GT Scribe is a web application, and can therefore be run on any computer or mobile device with an Internet browser. This application was developed using the most recent versions of Mozilla Firefox (47.0+) and Google Chrome (53.0+). We strongly recommend using one of these two browsers to access the application. The application runs locally, but does use the cloud for note storage, and therefore requires an Internet connection. Aside from this, any specific hardware configuration of your machine or mobile device should not be necessary.

This application is launched via Python3. To begin the installation process, you must first [install Python3](https://www.python.org/downloads/). 

------
**Dependent Libraries**

Before launching the application, you must install all of the application's dependent libraries. We recommend using the tool pip3 to download these libraries, as it came with the Python3 installation. Install these libraries by opening your machine's command line terminal and typing these commands, followed by the Enter key after each line. Each line installs one package.

1. `pip3 install Flask`
2. `pip3 install flask_restful`
3. `pip3 install flask-SQLAlchemy`
4. `pip3 install boto3`
5. `pip3 install flask-wtf`
6. `pip3 install flask-mail`

------
**Download and Build Instructions**

1. Find the Clone or Download button at the top of this Github page; click the button and select Download ZIP. ![Image of Download Button](http://i65.tinypic.com/z1x0m.png)
2. Unzip the file. Open the command line terminal and navigate to the top level of the newly unzipped file. (Same level where `manage.py` is.)
3. Create the database before running this for the first time. On the command line, type each these commands followed by the Enter key `python3 manage.py create_db`, `python3 manage.py populate_courses`, `python3 manage.py populate_users`. If there are any errors in this process, drop the database and then restart this step, `python3 manage.py drop_db`.
4. Start the server by typing this command `python3 serve.py`.
5. If prompted, allow any requests for incoming connections.
6. In your Internet browser, navigate to `localhost:5000` to see the rendered index page.
7. For working with the database, we recommend you download DB Browser for SQLite, which can be found [here](http://sqlitebrowser.org/). In the SQLite Browser, open the database (`temp.db`, inside the `data` folder) to view and directly edit its contents. Be sure to select "Write Changes" to save changes. If the script does not work, try manually making the `data` folder first, then running the script

-------
**Troubleshooting**

This application is launched via the command line. Therefore, all users are encouraged to refer to any logs in the command line terminal if the application does not seem to be working. These are the most commonly found problems with the application and installation process:

- If there is an error using pip3 to install any dependent libraries, your user account likely does not have administrator privileges on your machine. When this happens, try typing the word `sudo` at the beginning of each command, like so: `sudo pip3 install flask`. You may be asked to type in your password in order to complete the task--follow the onscreen directions; it is safe to type in your password. Hit Enter once you are done with each command, even if no typed characters appear on screen.
- If there are no courses on the course enrollment page, you probably forgot to populate the database the first time you installed the application. Please refer to Step 2 of the Download and Build Instructions.
- Account passwords are case sensitive, and caution should be taken to ensure you have typed your password correctly when registering/logging in.
- Web applications sometimes experience difficulties with caching information. If information you have input into the application does not seem to be showing up, try clearing your cache. [Clear your cache on Firefox](https://support.mozilla.org/en-US/kb/how-clear-firefox-cache); [Clear your cache on Chrome](https://support.google.com/accounts/answer/32050?hl=en)
- If an obvious error occurs within the application, and appear on-screen somewhat similar to [this](http://flask.pocoo.org/docs/0.11/_images/debugger.png), please contact an administrator.

----------
**Readme guidelines that can be deleted**

- Download instructions: how will the customer and users get access to the project?
- Build instructions (if needed): if you are providing the raw source code rather than a binary build, how will the customer and users create the required executable application
- Installation of actual application: what steps have to be taken after the software is built, what directories are required for installation
- Run instructions: what does the user/customer actually have to do to get the software to execute
- Troubleshooting: what are common errors that occur during installation and what is the corrective action
