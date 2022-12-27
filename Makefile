SHELL := /bin/bash

all: setup run

setup:
	python3 -m venv venv
	source venv/bin/activate
	pip install -r requirements.txt
	pip install git+https://github.com/openai/whisper.git
	deactivate

run:
	source venv/bin/activate
	python3 app.py
	deactivate