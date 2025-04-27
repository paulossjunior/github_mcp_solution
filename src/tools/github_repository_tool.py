import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional
import json

class GitHubRepositoryTool(BaseTool):
    name: str = "get_github_milestones"
    description: str = "Fetches milestones from a GitHub repository. Input: 'owner/repo'. Returns milestones as JSON string including number."

    def _run(self, query: str) -> str:
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        # Se o input for lista, pega o primeiro elemento
        if isinstance(query, list):
            query = query[0]

        # Limpar crases e espaços extras
        repo_path = query.replace("`", "").replace("\n", "").strip()

        # Validar formato
        if "/" not in repo_path:
            raise ValueError(f"Formato inválido: '{repo_path}'. Esperado 'owner/repo'.")

        url = f"https://api.github.com/repos/{repo_path}/milestones"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"GitHub API error {response.status_code}: {response.text}")

        milestones = response.json()

        formatted = [
            {
                "number": m.get("number", 0),  # <-- Agora inclui o número do milestone!
                "title": m.get("title", ""),
                "created_at": m.get("created_at", ""),
                "due_on": m.get("due_on", ""),
                "state": m.get("state", "")
            }
            for m in milestones
        ]

        return f"milestones: {json.dumps(formatted)}"

    def _arun(self, query: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
