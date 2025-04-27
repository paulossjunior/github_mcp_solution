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

        # Começa relatório
        markdown = f"# 📋 Relatório de Milestones e Issues do Repositório {query}\n\n"

        # --- RESUMO dos milestones
        markdown += "## 📈 Resumo dos Milestones\n\n"
        markdown += "| Número | Título | Criado em | Entrega Prevista | Tarefas Concluídas | Tarefas Abertas |\n"
        markdown += "|:------:|:-------|:----------|:-----------------|:------------------:|:---------------:|\n"

        for m in milestones:
            milestone_number = m.get('number')
            milestone_title = m.get('title')
            created_at = m.get('created_at')
            due_on = m.get('due_on') or 'N/A'

            # Filtra issues relacionadas
            related_issues = [i for i in issues if i.get('milestone_number') == milestone_number]

            # Conta issues concluídas e abertas
            closed_count = sum(1 for i in related_issues if i.get('state') == 'closed')
            open_count = sum(1 for i in related_issues if i.get('state') != 'closed')

            markdown += f"| {milestone_number} | {milestone_title} | {created_at} | {due_on} | {closed_count} | {open_count} |\n"

        # --- Detalhamento de milestones e issues
        markdown += "\n## 📋 Detalhamento dos Milestones e Issues\n\n"

        for m in milestones:
            markdown += f"### 📌 Milestone {m.get('number')} - {m.get('title')} ({m.get('state')})\n"
            markdown += f"- Criado em: {m.get('created_at')}\n"
            due = m.get('due_on') or 'N/A'
            markdown += f"- Entrega prevista: {due}\n\n"

            related = [i for i in issues if i.get('milestone_number') == m.get('number')]
            if related:
                markdown += "| Status | Título | Criado por | Atribuído para | Criada em | Fechada em |\n"
                markdown += "|:------:|:-------|:-----------|:---------------|:---------|:-----------|\n"
                for i in related:
                    status_emoji = "✅" if i.get('state') == "closed" else "🚧"
                    closed_at = i.get('closed_at') or "-"
                    markdown += (
                        f"| {status_emoji} | {i.get('title')} | {i.get('creator')} | {i.get('assignee')} | "
                        f"{i.get('created_at')} | {closed_at} |\n"
                    )
                markdown += "\n"
            else:
                markdown += "Nenhuma issue para este milestone.\n\n"

        return markdown

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported.")
