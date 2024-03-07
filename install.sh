#!/bin/bash

find . | grep -E "(__pycache__|\.eggs|\.pyc|\.pyo$)" | xargs rm -rf
docker-compose down -v
for volume in $(docker volume ls -f name=jairocloud_depositor -q); do
  docker volume rm $(volume)
done
DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose build --no-cache --force-rm

docker-compose up -d