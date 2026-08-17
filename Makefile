.PHONY: run build down test format lint

run:
	docker compose up --build

build:
	docker compose build

down:
	docker compose down

test:
	docker compose -f docker-compose.test.yml up --build --abort-on-container-exit --exit-code-from tests --remove-orphans

format:
    black app/ tests/ --line-length 120 --target-version py312 && isort app/ tests/ --profile black

lint:
    flake8 app/ tests/ && mypy app/ tests
