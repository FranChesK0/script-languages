.PHONY: run
run:
	python ./lab3/main.py

.PHONY: delete-db
delete-db:
	rm ./db/posts.db

.PHONY: rerun
rerun:
	make delete-db
	make run

DEFAULT_GOAL: run
