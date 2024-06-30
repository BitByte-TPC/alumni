# IIITDM Alumni Connect   
  This web application aims to facilitate the Alumni Affairs of IIITDM Jabalpur. Please read the contributing guidelines before starting.

## Requirements

 * Python: 3.9 and above
 * Django: 2.2.28 
 * And additional requirements are in [**requirements.txt**](./requirements.txt). These will automatically be installed with the below steps.

## Setting Up Python Environment with `pyenv`

* For Windows
  - Open Command Prompt (cmd) as an administrator.
  ```
  $ git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%\.pyenv
  $ setx PYENV "%USERPROFILE%\.pyenv"
  $ setx PATH "%PYENV%\bin;%PYENV%\shims;%PATH%"
  ```
  
* For Linux 
 - Open Terminal
   ```
   $ sudo apt update
   $ sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
   ```
- Run `$ curl https://pyenv.run | bash`
- Clone the repository `$ git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%\.pyenv`
- Add pyenv to your shell configuraion
  ```
  $ echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
  $ echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
  $ echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
  $ echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  ```
## How to run it?

  * Fork the repository.
  * Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/alumni.git`
  * Change directory to alumni `$ cd alumni`
  * Add a reference to the original repository `$ git remote add upstream https://github.com/BitByte-TPC/alumni.git`
  * Install the required version of Python for the project `$ pyenv install 3.9`
  * Set the local Python version for the project `$ pyenv local 3.9`
  * Install virtualenv `$ pip3 install virtualenv`  
  * Create a virtual environment `$ virtualenv env -p python3`
  * Activate the env: `$ source env/bin/activate` (for linux) `> ./env/Scripts/activate` (for Windows PowerShell)
  * Install the requirements: `$ pip install -r requirements.txt`  
    **Note:** If some requirement causes some error, remove the version from that requirement (ex. convert `anyjson==0.3.3` to `anyjson`) and run the above command again.
  * Make migrations `$ python manage.py makemigrations`
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
  
