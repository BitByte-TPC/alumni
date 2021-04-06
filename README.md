# IIITDM Alumni Connect   
  This web-application aims to facilitate the Alumni Affairs of IIITDM Jabalpur.
  Requires `python 3.6+` and `django 2.1.15+`.
  Must read contributing guidelines before starting.

## Requirements

 * Python: 3.6/3.7  
 * Django: 2.1.15  
 * And additional requirements are in [**requirements.txt**](./requirements.txt). These will automatically be installed with below steps.


## How to run it?

  * Install virtualenv `$ sudo apt install python-virtualenv`  
  * Create a virtual environment `$ virtualenv env -p python3.6`  
  * Activate the env: `$ source env/bin/activate`
  * Install mysql-client : `sudo apt-get install libmysqlclient-dev`
  * Install the requirements: `$ pip install -r requirements.txt`
  * Change directory to AluminiConnect `$ cd AluminiConnect`
  * Make migrations `$ python manage.py makemigrations`
  * To Make migrations for a particular app `$ python manage.py makemigrations <App name>`
  * Migrate the changes to the database `$ python manage.py migrate`
  * Run the server `$ python manage.py runserver`
  * Create admin `$ python manage.py createsuperuser`
  * Create tables `$ python manage.py migrate --run-syncdb`

## Contributing  
  * Create a new branch with a related name of the motive. Branch name should follow these conventions. 
    - `feature/*` if you're implementing a new feature or adding some new functionality.
    - `refactor/*` if you're refactoring code or upgrading anything.
    - `bug/*` if you've fixed a bug that's not deployed onto Production yet.
    - `hotfix/*` if you've fixed a bug that is deployed and/or causing problems in Production.
    - Note: DON'T push to `master` or `release` branch.
  * Use an IDE linter, like **SonarLint**, to fix common bugs/code quality issues. 
  * Update your task's status in the provided spreadsheet.
  * Send a pull request anytime :)  
  
