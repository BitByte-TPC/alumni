# IIITDM Alumini Connect   
  This web-application aims to facilitate the Alumini Affirs of IIITDM Jabalpur.
  Requires `python3.6+` and `django==1.11.18+`  

## Requirements

Python 3.6  
Django==1.11.18  
And additional requirements are in **requirements.txt**  


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
  * Create a new branch with a related name of the motive i.e. bug/refactor/feature  
  * Create an issue before actually starting to code  
  * Send a pull request anytime :)  
  
