import os
from langchain.tools import BaseTool
from typing import List, Dict
from service.github_issue_service import GitHubIssueService

class GitHubIssueTool(BaseTool):
    name: str = "get_github_issues"
    description: str = (
        "Fetches issues from a GitHub milestone. Input: 'owner/repo/milestone_number'. Returns a list of issue dicts including assignee, creator, state, dates."
    )

    def _run(self, query: str) -> List[Dict[str, str]]:
        token = os.getenv("GITHUB_TOKEN")

        if isinstance(query, list):
            query = query[0]

        repo_query = query.replace("`", "").replace("\n", "").strip()

        try:
            repo_path, milestone_str = repo_query.rsplit("/", 1)
            milestone_number = int(milestone_str)
        except ValueError:
            raise ValueError("Input inválido. Esperado formato 'owner/repo/milestone_number'.")

        token = os.getenv("GITHUB_TOKEN")
        service = GitHubIssueService()
        formatted = service.get_all(repo_path,milestone_number,token)
        
        return formatted

    def _arun(self, query: str) -> List[Dict[str, str]]:
        raise NotImplementedError("Async not supported.")
