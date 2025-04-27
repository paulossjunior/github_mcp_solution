import os
import requests
from typing import List, Dict, Any
from langchain.tools import BaseTool
from service.github_project_service import GitHubProjectService

class ListProjectsCardsMilestonesTool(BaseTool):
    name: str = "list_projects_cards_milestones"
    description: str = (
        "Fetches all GitHub Projects V2, repositories, milestones, and issues (with developers) for a given organization.\n"
        "Input: GitHub organization login."
    )

    def _run(self, organization: str) -> Dict[str, List[Dict[str, Any]]]:
        token = os.getenv("GITHUB_TOKEN")
        
        if not token:
            raise ValueError("GITHUB_TOKEN não encontrado nas variáveis de ambiente.")

        organization = organization.strip().replace("`", "").replace("\n", "")

        
        service = GitHubProjectService()
        result = service.get_all(token=token, login=organization)
        
        return {"projects": result}

    def _arun(self, organization: str) -> Dict[str, List[Dict[str, Any]]]:
        raise NotImplementedError("Async not supported.")
