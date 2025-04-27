import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
class GitHubIssueTool(BaseTool):
    name: str = "get_github_issues"
    description: str = "Fetches issues from a GitHub milestone. Input: 'owner/repo/milestone_number'. Saves issues to memory."

    def _run(self, query: str) -> str:
        from langchain.callbacks.manager import CallbackManagerForToolRun
        from langchain.schema import SystemMessage

        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        try:
            owner, repo, milestone_number = query.split("/")
            milestone_number = int(milestone_number)
        except ValueError:
            raise ValueError("Input must be 'owner/repo/milestone_number'.")

        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {"milestone": milestone_number, "state": "all"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code}")

        issues = response.json()
        formatted = [
            {
                "title": i.get("title", ""),
                "state": i.get("state", ""),
                "created_at": i.get("created_at", "")
            }
            for i in issues
        ]

        system_message = SystemMessage(content=f"issues: {formatted}")
        CallbackManagerForToolRun.on_chat_model_start(
            {},
            [system_message]
        )

        return f"{len(formatted)} issues armazenadas."

    def _arun(self, query: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
