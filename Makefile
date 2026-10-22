.PHONY: install run build lint publish-check

install:
	uv sync

run:
	uv run project

build:
	uv build

lint:
	uv run ruff check .


publish-check:
	uvx twine check dist/primitive_db-0.1.0-py3-none-any.whl dist/primitive_db-0.1.0.tar.gz

