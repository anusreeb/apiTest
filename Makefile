build:
		docker build . -t docker-api-test-v0.0

run:
		docker run -it -p 8081:8081 docker-api-test-v0.0
