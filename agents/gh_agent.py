import os
import requests
import zipfile
import tempfile
import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

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

def summarize_logs_with_ai(logs):
    """Use an AutoGen AssistantAgent to summarize logs."""
    # Initialize an AssistantAgent
    # agent = AssistantAgent(name="log_analyzer", role="An AI assistant to analyze workflow logs.")
    
    # Create an agent that uses the OpenAI GPT-4o model.
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        api_key=os.getenv('API_KEY'),
    )
    agent = AssistantAgent(
        name="log_analyzer",
        model_client=model_client,
        system_message="Analyze the following logs, describe found failures and provide possible explanations.",
    )


    # Provide logs as input and define a prompt
    input_text = "\n\n".join(logs)
    prompt = f"""You are analyzing workflow logs from a CI/CD pipeline. Summarize the main events, including:
    - Successes
    - Errors or failures
    - Warnings or unexpected behaviors

    Logs:
    {input_text}
    """

    async def assistant_run() -> None:
        response = await agent.on_messages(
            [TextMessage(content=prompt, source="user")],
            cancellation_token=CancellationToken(),
        )
        print(response.inner_messages)
        print(response.chat_message.content)

    asyncio.run(assistant_run())

    # response = agent.run(prompt=prompt)
    # return response

if __name__ == "__main__":
    try:
        # Step 1: Fetch and extract logs
        zip_path = fetch_workflow_logs(REPO_OWNER, REPO_NAME, WORKFLOW_RUN_ID)
        print(f"Logs downloaded and saved to: {zip_path}")
        logs = extract_logs(zip_path)
        print(f"Extracted {len(logs)} log files.")

        # Step 2: Summarize logs with AI
        summary = summarize_logs_with_ai(logs)
        
        # Step 3: Print the summary
        # print("Summary of Workflow Logs:")
        # print(summary)
    except Exception as e:
        print(f"Error: {e}")
