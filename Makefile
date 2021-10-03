VENV = venv
SYSTEM_PYTHON = $(shell which python3.9)
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

venv:
	$(SYSTEM_PYTHON) -m venv $(VENV)

lint:
	make reqs-dev
	$(VENV)/bin/pylint lepymo.py modules/

reqs:
	make venv
	$(PIP) install -r requirements.txt

reqs-dev:
	make venv
	$(PIP) install -r requirements.txt -r requirements_dev.txt
	
dist:
	make reqs-dev
	$(VENV)/bin/pyinstaller --onefile --windowed --icon=app.ico --version-file=version.txt lepymo.py
	
run:
	$(PYTHON) lepymo.py

clean:
	rm -rf __pycache__
	rm -rf $(VENV)
	rm -rf build
	rm -rf dist
	
.PHONY: venv run lint dev dist clean reqs reqs-dev
