import os
import requests
from langchain.tools import BaseTool
from typing import Dict, Any
import json
from .list_all_milestones_and_issues_tool import ListAllMilestonesAndIssuesTool
from service.github_repository_service import GitHubRepositoryService

class GenerateReportTool(BaseTool):
    name: str = "generate_full_markdown_report_repository"
    description: str = (
        "Fetches all milestones and issues for a given repository and generates a complete Markdown report. "
        "Input: 'owner/repo'."
    )

    def _run(self, query: str) -> str:
        
        # Chama a ferramenta que lista todos milestones e issues
        
        list_tool = ListAllMilestonesAndIssuesTool()
        raw = list_tool._run(query)

        # Se veio como string JSON, converte para dict
        try:
            data = json.loads(raw) if isinstance(raw, str) else raw
        except json.JSONDecodeError:
            raise ValueError("Formato inválido retornado pela ferramenta de listagem.")

        # Extrai dados
        milestones = data.get("milestones", []) if isinstance(data, dict) else []
        issues = data.get("issues", []) if isinstance(data, dict) else []


        if not milestones:
            return (
                "Desculpe, não foi possível gerar o relatório em Markdown pois nenhum milestone foi encontrado."
            )
        
        service = GitHubRepositoryService()

        return service.generate_milestone_issue_markdown_report(milestones,issues,query)

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported.")
