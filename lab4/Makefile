.PHONY: lint
lint:
	isort .
	black .
	flake8 .
	mypy .

.PHONY: clear-db
clear-db:
	rm ./db/posts.db

.PHONY: run
run:
	python ./src/main.py

.DEFAULT_GOAL := run
