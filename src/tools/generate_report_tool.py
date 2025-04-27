import os
import requests
from langchain.tools import BaseTool
from typing import Dict, Any
import json
from .list_all_milestones_and_issues_tool import ListAllMilestonesAndIssuesTool

class GenerateReportTool(BaseTool):
    name: str = "generate_full_markdown_report"
    description: str = (
        "Fetches all milestones and issues for a given repo and generates a complete Markdown report. "
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

        markdown = f"# 📋 Relatório de Milestones e Issues do Repositório {query}"

        for m in milestones:
            markdown += f"## 📌 Milestone {m.get('number')} - {m.get('title')} ({m.get('state')})"
            markdown += f"- Criado em: {m.get('created_at')}"
            due = m.get('due_on') or 'N/A'
            markdown += f"- Entrega prevista: {due}"

            # Filtra issues relacionadas a este milestone
            related = [i for i in issues if i.get('milestone_number') == m.get('number')]
            if related:
                markdown += "| Status | Título | Criado por | Atribuído para | Criada em | Fechada em |"
                markdown += "|:------:|:-------|:-----------|:---------------|:---------|:-----------|"
                for i in related:
                    status_emoji = "✅" if i.get('state') == "closed" else "🚧"
                    closed = i.get('closed_at') or "-"
                    markdown += (
                        f"| {status_emoji} | {i.get('title')} | {i.get('creator')} | {i.get('assignee')} | "
                        f"{i.get('created_at')} | {closed} |"
                    )
                markdown += ""
            else:
                markdown += "Nenhuma issue para este milestone."

        return markdown

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported.")
