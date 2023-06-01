.SHELLFLAGS := -eu -c
VENV_NAME = check-bookmarks

requirements.txt: requirements.in

requirements-dev.txt: requirements.txt requirements-dev.in

lock: requirements.txt requirements-dev.txt

sync:
	pew in $(VENV_NAME) pip-sync requirements.txt requirements-dev.txt

%.txt: %.in
	pip-compile --output-file $@ $<

install:
	pew new -p python3.11 -r requirements.txt -r requirements-dev.txt $(VENV_NAME)

.PHONY: install
