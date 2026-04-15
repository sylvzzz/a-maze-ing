CONFIG	= config.txt
MAIN	= a_maze_ing.py

build:
	pip install -r requirements.txt

install: build
	pip install build
	python3 -m build


run:
	python3 $(MAIN) $(CONFIG)

debug:
	python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +


lint:
	python3 -m flake8 . --exclude a-maze-ing
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	python3 -m flake8 . --exclude a-maze-ing
	python3 -m mypy . --strict --exclude a-maze-ing


.PHONY: build install run debug clean lint lint-strict