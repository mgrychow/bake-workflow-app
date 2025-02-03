from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

GITHUB_OWNER = "YOUR_GITHUB_OWNER"
GITHUB_REPO = "YOUR_GITHUB_REPO"

@app.route("/workflow-status", methods=["GET"])
def get_workflow_status():
    url = f"https://api.github.com/repos/mgrychow/bake-workflow-app/actions/runs"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch workflow statuses", "details": response.json()}), response.status_code
    
    data = response.json()
    runs = [{
        "id": run["id"],
        "name": run.get("name", "Unknown"),
        "status": run.get("status", "Unknown"),
        "conclusion": run.get("conclusion", "Unknown"),
        "branch": run.get("head_branch", "Unknown"),
        "commit_sha": run.get("head_sha", "Unknown"),
        "html_url": run.get("html_url", ""),
        "created_at": run.get("created_at", "Unknown"),
    } for run in data.get("workflow_runs", [])]
    
    return jsonify(runs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)