import requests
from typing import List, Dict

class GitHubIssueRepository():
    
    def get_all(self, repo_path, milestone_number, token):
        
        headers = {"Authorization": f"token {token}"}

        url = f"https://api.github.com/repos/{repo_path}/issues"
        params = {"milestone": milestone_number, "state": "all"}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"GitHub API error {response.status_code}: {response.text}")

        issues_data = response.json()
        
        formatted: List[Dict[str, str]] = []

        for i in issues_data:
            assignee_info = i.get("assignee")
            assignee_login = assignee_info.get("login") if assignee_info else "Não atribuído"
            creator_login = i.get("user", {}).get("login", "Desconhecido")

            formatted.append({
                "title": i.get("title", ""),
                "state": i.get("state", ""),
                "created_at": i.get("created_at", ""),
                "closed_at": i.get("closed_at", ""),
                "creator": creator_login,
                "assignee": assignee_login
            })

        return formatted