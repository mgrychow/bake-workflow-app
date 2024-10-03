# Bake Workflow

This Python application is designed to experiment on automating docker bake process with Github Actions

# Usage

## Native

1. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
2. Run the application:
    ```sh
    python main.py
    ```
3. Run tests:
    ```sh
    cd tests
    pytest
    ```
## Contenerized

1. Build
    ```
    docker build -t bake-workflow-app .
    ```
    Build with customized response
    ```
    docker build --build-arg PING_RESPONSE="hello" -t bake-workflow-app . 
    ```
2. Run 
    ```
    docker run -p 5000:5000 -d --name app bake-workflow-app
    ```
3. Stop
    ```
    docker stop app
    ```

## Query
    ```
    curl http://localhost:5000/ping
    ```

## Contributing

No