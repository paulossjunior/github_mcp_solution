import requests
from typing import List, Dict

class GitHubMilestoneRepository():
    
    def get_all(self, repo_path, token):
        
        headers = {"Authorization": f"token {token}"}

        url = f"https://api.github.com/repos/{repo_path}/milestones"
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API error {response.status_code}: {response.text}")

        data = response.json()
        formatted: List[Dict[str, str]] = []
        for m in data:
            formatted.append({
                "number": str(m.get("number", "")),
                "title": m.get("title", ""),
                "created_at": m.get("created_at", ""),
                "due_on": m.get("due_on", ""),
                "state": m.get("state", "")
            })
        return formatted
