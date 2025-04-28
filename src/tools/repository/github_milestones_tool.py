import os
from langchain.tools import BaseTool
from typing import List, Dict, Optional
from service.github_milestone_service import GitHubMilestoneService

class GitHubMilestoneTool(BaseTool):
    name: str = "get_github_milestones"
    description: str = "Fetches milestones from a GitHub repository. Input: 'owner/repo'. Returns a list of milestone dicts."

    def _run(self, query: str) -> List[Dict[str, str]]:
        
        if isinstance(query, list):
            query = query[0]

        repo_path = query.replace("`", "").replace("\n", "").strip()
        if "/" not in repo_path:
            raise ValueError(f"Formato inválido: '{repo_path}'. Esperado 'owner/repo'.")
        
        token = os.getenv("GITHUB_TOKEN")
        service = GitHubMilestoneService()
        formatted = service.get_all(repo_path,token)
        
        return formatted

    def _arun(self, query: str) -> Optional[List[Dict[str, str]]]:
        raise NotImplementedError("Async not supported.")
