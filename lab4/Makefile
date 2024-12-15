.PHONY: help format lint check delete-db run

.DEFAULT_GOAL := help

help:
	@echo "Usage: make [TARGET]"
	@echo "Targets:"
	@echo "  help       Display this help message"
	@echo "  format     Format code with Isort and Black"
	@echo "  lint       Lint code with Flake8 and MyPy"
	@echo "  check      Run format and lint targets"
	@echo "  delete-db  Delete database"
	@echo "  run        Run application"

format:
	isort .
	black .

lint:
	flake8 .
	mypy .

check: foramt lint

delete-db:
	rm ./posts.db

run:
	python ./main.py
