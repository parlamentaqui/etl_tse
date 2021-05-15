start-dev:
	docker-compose up

start-prod:
	docker-compose up --build --detach 

test:
	sudo docker run prlmntq_etl_tse  sh -c 'python  src/test.py'
