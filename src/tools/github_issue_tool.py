import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional
import json

class GitHubIssueTool(BaseTool):
    name: str = "get_github_issues"
    description: str = "Fetches issues from a GitHub milestone. Input: 'owner/repo/milestone_number'. Handles Markdown crases and list input."

    def _run(self, query: str) -> str:
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        # Se o input for lista, pega o primeiro elemento
        if isinstance(query, list):
            query = query[0]

        # Limpar crases, espaços, quebras de linha
        query = query.replace("`", "").replace("\n", "").strip()

        try:
            owner_repo, milestone_number = query.rsplit("/", 1)
            milestone_number = int(milestone_number)
        except ValueError:
            raise ValueError("Input inválido. Esperado formato 'owner/repo/milestone_number'.")

        url = f"https://api.github.com/repos/{owner_repo}/issues"
        params = {
            "milestone": milestone_number,
            "state": "all"
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"GitHub API error {response.status_code}: {response.text}")

        issues = response.json()

        formatted = [
            {
                "title": i.get("title", ""),
                "state": i.get("state", ""),
                "created_at": i.get("created_at", ""),
                "closed_at": i.get("closed_at", ""),
                "creator": i.get("user", {}).get("login", "Desconhecido"),
                "assignee": i["assignee"]["login"] if i.get("assignee") else "Não atribuído"
            }
            for i in issues
        ]

        return f"issues: {json.dumps(formatted)}"

    def _arun(self, query: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
