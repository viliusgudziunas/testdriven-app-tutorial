#!/bin/bash

fails=""

inspect() {
  if [ $1 -ne 0 ]; then
    fails="${fails} $2"
  fi
}

# run unit and integration tests
docker-compose up -d --build
docker-compose exec users python manage.py test
inspect $? users
docker-compose exec users flake8 . --exclude migrations
inspect $? users-lint
docker-compose exec client react-scripts test --coverage --watchAll=false
inspect $? client
docker-compose down

# run e2e tests
# docker-compose -f docker-compose-prod.yml up -d --build
# docker-compose -f docker-compose-prod.yml exec users python manage.py recreate_db
# ./node_modules/.bin/cypress run --config baseUrl=http://localhost
# ./node_modules/.bin/cypress run --config baseUrl=http://192.168.99.102/
# inspect $? e2e
# docker-compose -f docker-compose-prod.yml down
docker-compose up -d --build
./node_modules/.bin/cypress run
inspect $? e2e
docker-compose down

# return proper code
if [ -n "${fails}" ]; then
  echo "Tests failed: ${fails}"
  exit 1
else
  echo "Tests passed!"
  exit 0
fi