# AI Agent

This subfolder contains script that uses AI Chat assistant to check specific workflow run

# Running the app

1. Create and start virtual environment
    ```
    python -m venv .venv
    source .venv/bin/activate
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Fill .env file with github token and openAi api token
4. Run python server
    ```sh
    python -m http.server
    ```
4. Run the application:
    ```sh
    python gh_agent.py
    ```
    or 
    ```sh
    python ci_analyzer.py
    ```