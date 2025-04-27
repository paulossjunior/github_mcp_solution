import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional
import json

class ListAllMilestonesAndIssuesTool(BaseTool):
    name: str = "list_all_milestones_and_issues"
    description: str = (
        "Fetches all milestones and issues from a GitHub repository. "
        "Input: 'owner/repo'. Automatically collects milestones and their related issues."
    )

    def _run(self, query: str) -> str:
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        if isinstance(query, list):
            query = query[0]

        repo_path = query.replace("`", "").replace("\n", "").replace('"', "").replace("'", "").strip()

        if "/" not in repo_path:
            raise ValueError(f"Formato inválido: '{repo_path}'. Esperado 'owner/repo'.")

        # Buscar milestones
        milestones_url = f"https://api.github.com/repos/{repo_path}/milestones"
        milestones_response = requests.get(milestones_url, headers=headers)

        if milestones_response.status_code != 200:
            raise Exception(f"GitHub API error {milestones_response.status_code}: {milestones_response.text}")

        milestones_data = milestones_response.json()

        milestones = [
            {
                "number": m.get("number", 0),
                "title": m.get("title", ""),
                "created_at": m.get("created_at", ""),
                "due_on": m.get("due_on", ""),
                "state": m.get("state", "")
            }
            for m in milestones_data
        ]

        all_issues = []

        # Buscar issues de cada milestone
        for milestone in milestones:
            milestone_number = milestone["number"]
            issues_url = f"https://api.github.com/repos/{repo_path}/issues"
            params = {
                "milestone": milestone_number,
                "state": "all"
            }
            issues_response = requests.get(issues_url, headers=headers, params=params)

            if issues_response.status_code != 200:
                raise Exception(f"GitHub API error {issues_response.status_code}: {issues_response.text}")

            issues_data = issues_response.json()

            for i in issues_data:
                all_issues.append({
                    "title": i.get("title", ""),
                    "state": i.get("state", ""),
                    "created_at": i.get("created_at", ""),
                    "closed_at": i.get("closed_at", ""),
                    "creator": i.get("user", {}).get("login", "Desconhecido"),
                    "assignee": i["assignee"]["login"] if i.get("assignee") else "Não atribuído",
                    "milestone_number": milestone_number,
                    "milestone_title": milestone["title"]
                })

        result = {
            "milestones": milestones,
            "issues": all_issues
        }

        # 🛠️ Voltar texto legível
        return f"Dados coletados com sucesso:\n{json.dumps(result)}"

    def _arun(self, query: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")

