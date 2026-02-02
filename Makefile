# Makefile
.PHONY: install format test run docker-build

install:
	uv sync

format:
	uv run ruff check . --fix
	uv run ruff format .

test:
	uv run pytest

run:
	uv run python -m src.app

docker-build:
	docker build -t multimodal-ai .
