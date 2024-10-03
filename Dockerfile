# Use the official Python image from the Docker Hub
FROM python:3.9-slim
# Set the PING_RESPONSE build argument
ARG PING_RESPONSE="pong"

# Set the PING_RESPONSE environment variable from the build argument
ENV PING_RESPONSE=${PING_RESPONSE}

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["python", "app.py"]