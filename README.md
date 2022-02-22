# CinemaSite
This is a demo movie review site example

# A video demo available at:
https://www.loom.com/share/61b452bacc084b1a861220efc23e1221


# To start the site on your local
After cloning the repo to your local change to that directory and follow the steps below:


## Create a new virtualenv

    virtualenv venv
    
## Activate the virtualenv

    source venv/bin/activate (on Unix)
    venv/Scripts/activate (on Windows)

### Install the required packages from requirements.txt

    pip3 install -r requirements.txt

### If you want to work on a clean database delete 'db.sqlite3' and create another file of the same name and do the migrations (else skip to the last step):

    python manage.py makemigrations
    python manage.py migrate

### To create a superuser use

    python manage.py createsuperuser

### Instead, if you want to work on the default database admin credentials are as follows:
    username: mehmet
    password: mehSan123.

### To host the site use:
    python manage.py runserver

### and register for a new user or use the one I have provided above
