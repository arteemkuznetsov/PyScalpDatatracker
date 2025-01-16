.PHONY: run restart update

COMPOSE_FILE = docker-compose.yml

DOCKER_COMPOSE = docker compose -f


update:
	@if git pull | grep -q 'Already up to date.'; then \
		echo "No changes pulled from git, skipping build."; \
	else \
		echo "Changes detected, building Docker image..."; \
		docker build -t pyscalp-datatracker .; \
	fi
#run: update
#	@if docker ps -q --filter name=api | grep .; then \
#		docker stop api; \
#		docker rm -f api; \
#	fi
#	sudo docker-compose -f docker-compose-api.yml up -d
#	@if docker ps -q --filter name=worker | grep .; then \
#		docker stop worker; \
#		docker rm -f worker; \
#	fi
#	sudo docker-compose -f docker-compose-worker.yml up -d
run:
	git pull
	$(DOCKER_COMPOSE) $(COMPOSE_FILE) up --build -d	

restart:
	$(foreach file, $(COMPOSE_FILE), $(DOCKER_COMPOSE) $(file) up --build -d;)

stop:
	$(foreach file, $(COMPOSE_FILE), $(DOCKER_COMPOSE) $(file) down;)

clean:
	docker image prune -f

#logs:
#	docker compose -f docker-compose-api.yml logs
#	docker compose -f docker-compose-worker.yml logs
