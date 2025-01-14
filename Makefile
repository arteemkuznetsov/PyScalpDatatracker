.PHONY: run restart update

COMPOSE_FILES = docker-compose-db.yml docker-compose-api.yml docker-compose-worker.yml

DOCKER_COMPOSE = sudo docker compose -f


update:
	@if git pull | grep -q 'Already up to date.'; then \
		echo "No changes pulled from git, skipping build."; \
	else \
		echo "Changes detected, building Docker image..."; \
		docker build -t pyscalp-datatracker-api:latest .; \
		docker build -t pyscalp-datatracker-worker .; \
	fi
run: update
	@if docker ps -q --filter name=api | grep .; then \
		docker stop api; \
		docker rm -f api; \
	fi
	sudo docker-compose -f docker-compose-api.yml up -d
	@if docker ps -q --filter name=worker | grep .; then \
		docker stop worker; \
		docker rm -f worker; \
	fi
	sudo docker-compose -f docker-compose-worker.yml up -d
run:
	git pull
	$(DOCKER_COMPOSE) docker-compose-db.yml up --build -d	
	$(DOCKER_COMPOSE) docker-compose-api.yml up --build -d
	$(DOCKER_COMPOSE) docker-compose-worker.yml up --build -d

restart:
	$(foreach file, $(COMPOSE_FILES), $(DOCKER_COMPOSE) $(file) up --build -d;)

stop:
	$(foreach file, $(COMPOSE_FILES), $(DOCKER_COMPOSE) $(file) down;)

clean:
	sudo docker image prune -f

logs:
	sudo docker compose -f docker-compose-api.yml logs
	sudo docker compose -f docker-compose-worker.yml logs
