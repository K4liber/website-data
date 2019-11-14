.SILENT:
.DEFAULT_GOAL := install

## Installs a development environment
install:
	docker-compose -f api/docker-compose.yml build
	docker-compose -f api/docker-compose.yml down -v
	docker-compose -f api/docker-compose.yml up -d --force-recreate

develop:
	docker-compose -f api/docker-compose.dev.yml build
	docker-compose -f api/docker-compose.dev.yml down -v
	docker-compose -f api/docker-compose.dev.yml up -d --force-recreate

test:
	docker-compose -f api/docker-compose.dev.yml run --rm --entrypoint pytest api $*