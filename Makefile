# -*- coding: utf-8 -*-
.PHONY: clean-pyc clean-build clean

help:
	@echo "clean - remove all build, test, coverage and Python artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "release - package and upload a release"
	@echo "dist - package"
	@echo "install - install the package to the active Python's site-packages"

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -rf {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

# clean-test:
# 	rm -fr .tox/
# 	rm -f .coverage
# 	rm -fr htmlcov/


test:
	pip install -r requirements.txt
	python setup.py test

# test-all:
# 	tox

# coverage:
# 	coverage run --source anicli setup.py test
# 	coverage report -m
# 	coverage html
# 	open htmlcov/index.html

# docs:
# 	rm -f docs/pipreqs.rst
# 	rm -f docs/modules.rst
# 	sphinx-apidoc -o docs/ pipreqs
# 	$(MAKE) -C docs clean
# 	$(MAKE) -C docs html
# 	open docs/_build/html/index.html

release: clean
	python setup.py sdist bdist_wheel upload -r pypi

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean
	python setup.py install