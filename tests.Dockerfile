# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Copy the current directory contents into the container at /app
COPY . /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install pytest for running tests
RUN pip install pytest

# Set environment variable for testing
ENV PING_RESPONSE="test_response"

WORKDIR /app/tests

# Run tests when the container launches
CMD ["pytest"]
