SHELL := /bin/bash
PNAME=paco
clean-pyc:
	find . -name '*.pyc' -exec rm -f {}

build:
	python3 -m build

clean:
	rm -rf dist
	rm -rf *.egg-info

test:
	tox

new-venv:
	( \
	virtualenv ./venv; \
	source ./venv/bin/activate; \
	python3 -m pip install -e ./dist/${PNAME}-*.tar.gz; \
	deactivate; \
	)

evenv:
	( \
	virtualenv ./venv; \
	source ./venv/bin/activate; \
	python3 -m pip install -e .; \
	deactivate; \
	)

clean-venv:
	rm -rf ./venv

help:
	@echo "--> clean-pyc:"
	@echo "        To clean the files with the extension pyc."
	@echo "--> build:"
	@echo "        Use this to build the package."
	@echo "--> clean-build:"
	@echo "        Use htis to clean build files."
	@echo "--> test:"
	@echo "        To simply make test with tox."
	@echo "--> new-venv:"
	@echo "        Creates a new venv with the current build."
	@echo "--> clean-venv:"
	@echo "        Cleans the virtual env. files."

