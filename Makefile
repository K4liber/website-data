.SILENT:
.DEFAULT_GOAL := install

## Installs a development environment
install:
	docker-compose -f deployments/docker-compose.yml build
	docker-compose -f deployments/docker-compose.yml down -v
	docker-compose -f deployments/docker-compose.yml up -d --force-recreate