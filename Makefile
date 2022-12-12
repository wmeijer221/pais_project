all: up clean

up: build
	docker-compose up --force-recreate

build:
	docker-compose build

clean:
	docker-compose down --rmi local
