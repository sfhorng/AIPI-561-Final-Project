install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

format:
	black .

lint:
	pylint --disable=R,C src/movie_chatbot tests

test:
	python -m pytest -vv --cov=src/movie_chatbot tests

all: install lint format test

start_model:
	sh -c ./TinyLlama-1.1B-Chat-v1.0.F16.llamafile

run_app:
	streamlit run src/movie_chatbot/app.py
