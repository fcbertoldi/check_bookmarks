.SHELLFLAGS := -eu -c
VENV_NAME = check-bookmarks

requirements.txt: pyproject.toml
	pip-compile -o requirements.txt pyproject.toml

requirements-dev.txt: requirements.txt pyproject.toml
	pip-compile --extra dev -o requirements-dev.txt requirements.txt pyproject.toml

lock: requirements.txt requirements-dev.txt

sync:
	pew in $(VENV_NAME) pip-sync requirements.txt requirements-dev.txt

install:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt $(VENV_NAME)

.PHONY: install
