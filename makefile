SRC = url_hostname tests setup.py

all: test


.install-deps: $(shell find requirements -type f)
	@pip install -U -r requirements/dev.txt
	@touch .install-deps

.develop: .install-deps $(shell find url_hostname -type f)
	@pip install -e .
	@touch .develop

flake8:
	flake8 $(SRC)

black-check:
	black --check --diff -t py35 $(SRC)

mypy:
	mypy --show-error-codes url_hostname tests

lint: flake8 black-check mypy

fmt:
	black -t py35 $(SRC)


test: lint .develop
	pytest ./tests ./url_hostname


vtest: lint .develop
	pytest ./tests ./url_hostname -v


cov: lint .develop
	pytest --cov url_hostname --cov-report html --cov-report term ./tests/ ./url_hostname/
	@echo "open file://`pwd`/htmlcov/index.html"


doc: doctest doc-spelling
	make -C docs html SPHINXOPTS="-W -E"
	@echo "open file://`pwd`/docs/_build/html/index.html"


doctest: .develop
	make -C docs doctest SPHINXOPTS="-W -E"


doc-spelling:
	make -C docs spelling SPHINXOPTS="-W -E"