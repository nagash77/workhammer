#Work RPG (tentative title)

Webapp backend for an idea on how to reward work.  Using an RPG like system of
giving experience and leveling up people for their roles (or classes) based on
accomplishments during their work.  For a better outline of the project, check out
the (docs)[docs/intro.md].

##Technical stuff

The app is written using Python 2.7 with Flask for the web framework and MongoDB as
the database backend.  It will provide an adaptive RESTful API along with a simple
backend generated HTML interface (to start).  It is written to use virtualenv.  It
will be done with good test coverage and against the flake8 (pyflakes + PEP8)
linting utility.

##Setup

For setup, if you have virtualenvwrapper and make installed you can just run:
```
make init
```

For those who do not, you can make a virtualenv (I recommend something like .env or
venv), activate it, then pip install the requirements, copy the template settings
file (described below), and it should be good to go.  (I would like to write a
better setup script, probably a setup.py file at some point).  So for Linux:
```
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
cp rpg/settings.py_template rpg/settings.py
python serve.py
```

## Settings

The app settings live in the rpg/settings.py.  I have included a
(template)[rpg.settings.py_template].  The file holds various settings for how the
application should behave, more settings will be added as functionality and
features get added (like when I get around to making the logging at a production
level capacity).  The current settings are:
* **DEBUG** straight forward, boolean that enables debugging settings
* **SECRET_KEY** this is a string that is used as part of the salt in password
  hashes
* **MONGO_HOST** dictionary that describes the URI of the mongodb instance to be
  used, keys are 'host' (the address of the machine) and 'port' (the port the
  service is listening on)
* **DEFAULT_SESSION** dictionary (temporary for now) that defines the defaults for
  a newly created session, mostly will be things like the default number of items
  returned for large lists (paginated) and the default datetime format.  (nothing
  for now)
