start-dev:
	docker-compose up

start-prod:
	docker-compose up --build --detach 

test:
	sudo docker-compose run prlmntq_etl_tse python  src/test.py
