install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black .

lint:
	pylint --disable=R,C src/movie_chatbot tests

test:
	python -m pytest -vv -s --cov=src/movie_chatbot tests

setup_all: install lint format test

start_model:
	sh -c ./TinyLlama-1.1B-Chat-v1.0.F16.llamafile

# Create image with latest build tag
build_local:
	docker build -t st_movie_chatbot .

# Start container from created image
# Mount vector store to app directory in container
# Absolute local path is needed for mounting files
# Connect to machine's localhost to retrieve from Llamafile
start_container_local:
	docker run --add-host=host.docker.internal:host-gateway \
	-v $(PWD)/vector_store:/app/vector_store \
	-p 8501:8501 st_movie_chatbot

