.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	mypy .

.PHONY: pre-commit
pre-commit:
	pre-commit run --all-files

.PHONY: run
run:
	python ./src/main.py

DEFAULT_GOAL: run

