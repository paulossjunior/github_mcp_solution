import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional

class GitHubRepositoryTool(BaseTool):
    name: str = "get_github_milestones"
    description: str = "Fetches milestones from a GitHub repository. Input: 'owner/repo'. Returns a list of milestone dicts."

    def _run(self, query: str) -> List[Dict[str, str]]:
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        if isinstance(query, list):
            query = query[0]

        repo_path = query.replace("`", "").replace("\n", "").strip()
        if "/" not in repo_path:
            raise ValueError(f"Formato inválido: '{repo_path}'. Esperado 'owner/repo'.")

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

    def _arun(self, query: str) -> Optional[List[Dict[str, str]]]:
        raise NotImplementedError("Async not supported.")
