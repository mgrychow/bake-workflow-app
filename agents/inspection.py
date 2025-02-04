import requests
import os
# from dotenv import load_dotenv
from datetime import datetime, timedelta

# GitHub API details
REPO_OWNER = "mgrychow"  # e.g., "octocat"
REPO_NAME = "bake-workflow-app"    # e.g., "Hello-World"
WORKFLOW_RUN_ID = "12853141825"  # Replace with a specific run ID

# load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_workflows():
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {url}:", response.json())
        return None
    
def get_workflow_id(workflow_name, workflows_json):
    workflows = workflows_json.get("workflows", [])
    for workflow in workflows:
        if workflow["name"] == workflow_name:
            return workflow["id"]
    return None

def get_workflow_runs(workflow_id):
    last_week = datetime.now() - timedelta(days=6)
    previous_day = last_week.strftime("%Y-%m-%d")
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/{workflow_id}/runs?created={previous_day} "
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {url}:", response.json())
        return None

def get_workflow_run_logs(workflow_run_id):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/runs/{workflow_run_id}/logs"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to retrieve data from {url}:", response.json())
        return None

def generate_workflow_report(workflow_runs):
    if not workflow_runs:
        return "No workflow runs found."
    report = "Workflow runs in the last week:\n"
    for run in workflow_runs.get("workflow_runs", []):
        report += f"Run ID: {run['id']}, Status: {run['status']}, Conclusion: {run['conclusion']}\n"
        report += f"Run URL: {run['html_url']}, Created at: {run['created_at']}\n\n"
        latest_run_id = workflow_runs["workflow_runs"][0]["id"]
        logs = get_workflow_run_logs(latest_run_id)
        if logs:
            if not os.path.exists("artifacts"):
                os.makedirs("artifacts")
            log_file_path = f"artifacts/workflow_run_{latest_run_id}_logs.zip"
            with open(log_file_path, "wb") as log_file:
                log_file.write(logs)
            report += f"Logs saved to {log_file_path}\n"
    report_file_path = f"artifacts/report.txt"
    with open(report_file_path, "w") as report_file:
        report_file.write(report)
    report += f"Report saved to {report_file_path}\n"
    return report

if __name__ == "__main__":
    workflow_name = "build images"
    workflow_id = None
    workflow_runs = None
    workflows_json = get_workflows()
    if workflows_json:
        workflow_id = get_workflow_id(workflow_name, workflows_json)
    if workflow_id:
        workflow_runs = get_workflow_runs(workflow_id)
    if workflow_runs:
        print(generate_workflow_report(workflow_runs))
    else:
        print("Error.")
    