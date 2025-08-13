PY ?= python
PIP ?= pip
VENV ?= .venv
ACTIVATE = . $(VENV)/bin/activate

.PHONY: install run-demo run-ui test clean

install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run-demo:
	$(PY) run_demo.py

run-ui:
	streamlit run app.py

test:
	$(PY) -m pytest -q

clean:
	rm -rf __pycache__ .pytest_cache dist build *.egg-info **/__pycache__
