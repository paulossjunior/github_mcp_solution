import os
import json
from langchain.tools import BaseTool
from typing import Dict, Any, List
from .list_all_milestones_and_issues_tool import ListAllMilestonesAndIssuesTool
from service.github_repository_service import GitHubRepositoryService

class GenerateDevelopersReportTool(BaseTool):
    name: str = "generate_developers_markdown_report"
    description: str = (
        "Fetches all milestones and issues for a given repo and generates a Markdown report grouped by developer. "
        "Input: 'owner/repo'."
    )

    def _run(self, query: str) -> str:
        
        # Chama a ferramenta que lista todos milestones e issues
        list_tool = ListAllMilestonesAndIssuesTool()
        raw = list_tool._run(query)

        try:
            data = json.loads(raw) if isinstance(raw, str) else raw
        except json.JSONDecodeError:
            raise ValueError("Formato inválido retornado pela ferramenta de listagem.")

        issues = data.get("issues", [])

        if not issues:
            return "Desculpe, não há issues para gerar o relatório."

        service = GitHubRepositoryService()
        return service.generate_developer_markdown_report(issues,query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported.")
