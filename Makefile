.PHONY: test run down

test:
	docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit --remove-orphans

run:
	docker-compose up --build

down:
	docker-compose down
