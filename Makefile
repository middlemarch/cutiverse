ENV_DIR=.env
PYTHON=python3

ifeq ($(OS),Windows_NT)
	IN_ENV=. $(ENV_DIR)/Scripts/activate &&
else
	IN_ENV=. $(ENV_DIR)/bin/activate &&
endif

# Some distros need to use pip3 as the entrypoint
ifneq (, $(shell which pip3))
PIP_CMD=pip3
else ifneq (, $(shell which pip))
PIP_CMD=pip
else
$(error "Python's pip not found on $(PATH)")
endif

all: test lint docs artifacts

env: $(ENV_DIR)

test: build
	$(IN_ENV) tox

artifacts: build-reqs sdist wheel

$(ENV_DIR):
	virtualenv -p $(PYTHON) $(ENV_DIR)

build-reqs: env
	$(IN_ENV) $(PIP_CMD) install build sphinx wheel twine setuptools_scm

build: build-reqs
	$(IN_ENV) $(PIP_CMD) install --editable .[dev]

sdist: build-reqs
	$(IN_ENV) $(PYTHON) -m build --no-isolation --sdist

wheel: build-reqs
	$(IN_ENV) $(PYTHON) -m build --no-isolation --wheel

format-code:
	$(IN_ENV) black -l 119 src/ docs/source/conf.py setup.py

check-code:
	$(IN_ENV) black --check -l 119 src/ docs/source/conf.py setup.py

docs: build-reqs
	$(IN_ENV) $(PIP_CMD) install -r docs/requirements.txt
	$(IN_ENV) $(MAKE) -C docs html

publish: artifacts
	$(IN_ENV) twine upload dist/*

freeze: env
	- $(IN_ENV) $(PIP_CMD) freeze

clean:
	- @rm -rf BUILD
	- @rm -rf BUILDROOT
	- @rm -rf RPMS
	- @rm -rf SRPMS
	- @rm -rf SOURCES
	- @rm -rf docs/build
	- @rm -rf src/*.egg-info
	- @rm -rf build
	- @rm -rf dist
	- @rm -f .coverage
	- @rm -f test_results.xml
	- @rm -f coverage.xml
	- @rm -f tests/coverage.xml
	- @rm -f pep8.out
	- find -name '*.pyc' -delete
	- find -name '*.pyo' -delete
	- find -name '*.pyd' -delete
	- find -name '*__pycache__*' -delete

env-clean: clean
	- @rm -rf .env*
	- @rm -rf $(ENV_DIR)
	- @rm -rf .tox
