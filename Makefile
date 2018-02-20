
SHELL = /bin/bash

all: build

build:
	docker build --tag lambda:latest .
	docker run --name lambda -itd lambda:latest
	docker cp lambda:/tmp/package.zip package.zip
	docker stop lambda
	docker rm lambda


shell:
	docker run \
		--name lambda  \
		--volume $(shell pwd)/:/data \
		--rm \
		-it \
		lambda:latest /bin/bash

clean:
	docker stop lambda
	docker rm lambda
