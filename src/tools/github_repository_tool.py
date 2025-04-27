import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()
class GitHubRepositoryTool(BaseTool):
    name: str = "get_github_milestones"
    description: str = "Fetches milestones from a GitHub repository. Input: 'owner/repo'. Saves milestones to memory."

    def _run(self, query: str) -> str:
        from langchain.callbacks.manager import CallbackManagerForToolRun
        from langchain.schema import SystemMessage

        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}"}

        try:
            owner, repo = query.split("/")
        except ValueError:
            raise ValueError("Input must be 'owner/repo'.")

        url = f"https://api.github.com/repos/{owner}/{repo}/milestones"
        print (url)
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API error: {response.status_code}")

        milestones = response.json()
        formatted = [
            {
                "title": m.get("title", ""),
                "created_at": m.get("created_at", ""),
                "due_on": m.get("due_on", ""),
                "state": m.get("state", "")
            }
            for m in milestones
        ]

        # Armazenar como SystemMessage
        system_message = SystemMessage(content=f"milestones: {formatted}")
        CallbackManagerForToolRun.on_chat_model_start(
            {},  # Sem kwargs
            [system_message]
        )

        return f"{len(formatted)} milestones armazenados."

    def _arun(self, query: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
