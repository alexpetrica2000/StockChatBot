APP_NAME=lseg-chatbot
PORT=8000

build:
	docker build -t $(APP_NAME) .

run:
	docker run -d -p $(PORT):8000 --name $(APP_NAME) $(APP_NAME)

logs:
	docker logs -f $(APP_NAME)

stop:
	docker stop $(APP_NAME) || true
	docker rm $(APP_NAME) || true