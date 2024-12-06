PYTHON = python3

.PHONY: help
help:
	@echo "  install     install all dev and production dependencies (virtualenv is created as venv)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style"
	@echo "  test        run tests"
	@echo "  coverage    run tests with code coverage"

.PHONY: install
install:
	$(PYTHON) -m venv venv; . venv/bin/activate; $(PYTHON) -m pip install -r dev-requirements.txt

.PHONY: clean
clean:
	rm -fr venv

.PHONY: lint
lint:
	@. venv/bin/activate; find . -iname "*.py" -not -path "./venv/*" -not -path "./test/*" -exec echo "Linting {}" \; -exec pylint -rn {} \;

.PHONY: test
test:
	@. venv/bin/activate; pytest -v --junitxml test/tests.xml

.PHONY: test-docker
test-docker:
	sh ci/test_with_docker.sh

.PHONY: coverage
coverage:
	@. venv/bin/activate; pytest --cov-report xml:test/coverage/cobertura-coverage.xml --cov=gen_edgerc --cov=httpie_edgegrid test/

.PHONY: all
all: clean install lint test coverage