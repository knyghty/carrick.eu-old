all: lint test

bandit:
	bandit -r . -c bandit.yml

black:
	black --check .

doc8:
	doc8 README.rst

flake8:
	flake8

isort:
	isort -c

lint: bandit black doc8 flake8 isort

test:
	pytest
