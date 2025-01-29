from autogen_core.tools import FunctionTool
from autogen_core.models import UserMessage
from autogen_core import CancellationToken
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient
from typing_extensions import Annotated
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import tempfile
import zipfile
from bs4 import BeautifulSoup
import asyncio
import os
import random

load_dotenv()

# GitHub API details
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = "mgrychow"  # e.g., "octocat"
REPO_NAME = "bake-workflow-app"    # e.g., "Hello-World"
WORKFLOW_RUN_ID = "12853141825"  # Replace with a specific run ID

def fetch_workflow_logs(repo_owner, repo_name, run_id):
    """Download logs for a specific workflow run."""
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/runs/{run_id}/logs"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    response = requests.get(api_url, headers=headers, stream=True)
    
    if response.status_code != 200:
        raise Exception(f"Error fetching logs: {response.status_code} - {response.json()}")
    
    # Save logs to a temporary file
    temp_zip_path = tempfile.mktemp(suffix=".zip")
    with open(temp_zip_path, "wb") as f:
        f.write(response.content)
    return temp_zip_path

def extract_logs(zip_path):
    """Extract logs from the ZIP file, including logs within directories."""
    extracted_logs = []
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        temp_dir = tempfile.mkdtemp()
        zip_ref.extractall(temp_dir)
        for root, _, files in os.walk(temp_dir):
            for log_file in files:
                with open(os.path.join(root, log_file), "r", encoding="utf-8") as f:
                    extracted_logs.append(f.read())
    return extracted_logs

async def get_logs(run_number: int) -> str:
    zip_path = fetch_workflow_logs(REPO_OWNER, REPO_NAME, run_number)
    print(f"Logs downloaded and saved to: {zip_path}")
    logs = extract_logs(zip_path)
    return(logs)

getlogs_tool = FunctionTool(get_logs, description="Get the logs of specific workflow run number.")

agent_state = None
openai_model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv('API_KEY'), # Optional if you have an OPENAI_API_KEY environment variable set.
)
agent = AssistantAgent(
    name="Pszemek",
    model_client=openai_model_client,
    tools=[getlogs_tool],
    system_message="Be a helpful assistant, provide concise and precise answers!",
)

async def main():
    app = Flask(__name__)
    CORS(app)

    @app.route('/query', methods=['POST'])
    async def query():
        global agent

        data = request.json
        prompt = data.get('prompt', '')
        try:
            result = await agent.on_messages([UserMessage(content=prompt, source="user")], CancellationToken())
            return jsonify({'response': result.chat_message.content})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    app.run(debug=True)

asyncio.run(main())