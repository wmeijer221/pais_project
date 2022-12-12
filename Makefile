all: up clean

up: build
	docker-compose up --force-recreate

build: clean
	docker-compose build

clean:
	docker-compose down --rmi local
