import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional
from service.github_project_service import GitHubProjectService

class GitHubProjectsV2Tool(BaseTool):
    name: str = "list_github_projects_v2"
    description: str = (
        "Fetches all GitHub Projects V2 for a given organization or user.\n"
        "Input: GitHub organization or user login."
    )

    def _run(self, login: str) -> List[Dict[str, str]]:
        token = os.getenv("GITHUB_TOKEN")
        
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set.")

        
        login = login.strip().replace("`", "").replace("\n", "")

        service = GitHubProjectService()

        return service.get_all(token=token, login=login)
        
        

    def _arun(self, login: str) -> Optional[List[Dict[str, str]]]:
        raise NotImplementedError("Async not supported.")
