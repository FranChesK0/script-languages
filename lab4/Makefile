.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	mypy .

.PHONY: run
run:
	python ./src/main.py

DEFAULT_GOAL: run

