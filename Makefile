# This tries to find a python linter, defaults to the NOP if none found
# Looks for: pyflakes and flake8 (for now)
LINTER=$(shell if which flake8 > /dev/null ; \
		then which flake8; \
		elif which pyflakes > /dev/null ; \
		then which pyflakes; \
		else which true; fi )
# This tries to figure out the virtualenv setup, if already in a virtualenv, uses
# NOP, if it finds mkvirtualenv, uses that, otherwise nothing (uses the global
# environment for now)
VENV=$(shell if $VIRTUAL_ENV > /dev/null ; \
	then which true; \
	else if which mkvirtualenv > /dev/null ; \
	then which mkvirtualenv; \
	else which true;) # Need to figure out default

init:
	${VENV} rpg
	pip install -r requirements.txt

unittest:
	nosetests --with-color ./tests/*.py

lint:
	${LINTER} ./rpg/*.py
	${LINTER} ./rpg/database/*.py

test: lint unittest

serve:
	python -m rpg
