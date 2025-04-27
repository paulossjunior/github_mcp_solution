import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional

class GitHubIssueTool(BaseTool):
    name: str = "get_github_issues"
    description: str = (
        "Fetches issues from a GitHub milestone. Input: 'owner/repo/milestone_number'. Returns a list of issue dicts including assignee, creator, state, dates."
    )

    def _run(self, query: str) -> List[Dict[str, str]]:
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        if isinstance(query, list):
            query = query[0]

        repo_query = query.replace("`", "").replace("\n", "").strip()

        try:
            owner_repo, milestone_str = repo_query.rsplit("/", 1)
            milestone_number = int(milestone_str)
        except ValueError:
            raise ValueError("Input inválido. Esperado formato 'owner/repo/milestone_number'.")

        url = f"https://api.github.com/repos/{owner_repo}/issues"
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

    def _arun(self, query: str) -> List[Dict[str, str]]:
        raise NotImplementedError("Async not supported.")
