# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the PING_RESPONSE build argument
ARG PING_RESPONSE="pong"

# Set the PING_RESPONSE environment variable from the build argument
ENV PING_RESPONSE=${PING_RESPONSE}

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest for running tests
RUN pip install pytest

WORKDIR /app/tests

# Run tests when the container launches
CMD ["pytest"]
