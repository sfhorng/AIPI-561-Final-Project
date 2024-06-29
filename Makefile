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

# Without Docker 
run_app:
	streamlit run src/movie_chatbot/app.py

# -----------------------------------------

# With Docker

# Create image with latest build tag
build:
	docker build -t st_movie_chatbot .

# Start container from created image
# Mount Llamafile to app directory in container
# Absolute local path is needed for mounting files
start_container:
	docker run -v $(PWD)/TinyLlama-1.1B-Chat-v1.0.F16.llamafile:/app/TinyLlama-1.1B-Chat-v1.0.F16.llamafile -p 8501:8501 st_movie_chatbot
