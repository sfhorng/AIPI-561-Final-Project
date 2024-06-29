# Use base image
FROM python:3.9-slim

# Environment setup preparation
COPY ./requirements.txt /app/requirements.txt

# Set the working directory for following instructions: 
# RUN, CMD, ENTRYPOINT, COPY, ADD
WORKDIR /app

# Environment setup
# Requirements for running the app
RUN pip install -r requirements.txt

# Install app logic
COPY src/* /app

# Streamlit apps use port 8501 by default
EXPOSE 8501

# Configure a container to run as an executable
# Structure: command, param1, param2 
ENTRYPOINT ["streamlit", "run", "app.py"]

