.PHONY: run restart update

COMPOSE_FILE = docker-compose.yml
COMPOSE_FILE_DB = ./infra/db/docker-compose.yml

DOCKER_COMPOSE = docker compose -f

build:
	git pull
	docker build -t pyscalp-datatracker:latest .

init: build
	mkdir -p ./infra/db/db_data
	$(DOCKER_COMPOSE) $(COMPOSE_FILE_DB) up -d

update:
	git pull
	docker build -t pyscalp-datatracker .

run:
	git pull
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up --build -d	

restart:
	$(foreach file, $(COMPOSE_FILE), $(DOCKER_COMPOSE) $(file) up --build -d;)

rebuild-api: update
	docker-compose rm -f -s -v api
	docker-compose up -d --no-deps --build api

rebuild-worker: update
	docker-compose rm -f -s -v worker
	docker-compose up -d --no-deps --build worker

db-upgrade: rebuild-api
	docker exec -i api alembic upgrade head

stop:
	$(foreach file, $(COMPOSE_FILE), $(DOCKER_COMPOSE) $(file) down;)

clean:
	docker image prune -f
