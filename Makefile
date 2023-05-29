.SHELLFLAGS := -eu -o pipefail -c


requirements.txt: pyproject.toml
	pip-compile -o requirements.txt pyproject.toml

requirements-dev.txt: pyproject.toml
	pip-compile --extra dev -o requirements-dev.txt pyproject.toml

lock: requirements.txt requirements-dev.txt

install:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt check-bookmarks

.PHONY: install
