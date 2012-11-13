LINTER=$(shell if which flake8 > /dev/null ; \
		then which flake8; \
		elif which pyflakes > /dev/null ; \
		then which pyflakes; \
		else which true; fi )

unittest:
	nosetests ./tests/*.py

lint:
	${LINTER} ./rpg/*.py
	${LINTER} ./rpg/database/*.py

test: lint unittest
