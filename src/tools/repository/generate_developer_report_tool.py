import os
import json
from langchain.tools import BaseTool
from typing import Dict, Any, List
from .list_all_milestones_and_issues_tool import ListAllMilestonesAndIssuesTool

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

        milestones = data.get("milestones", [])
        issues = data.get("issues", [])

        if not issues:
            return "Desculpe, não há issues para gerar o relatório."

        # Agrupar issues por assignee
        developers: Dict[str, List[Dict[str, Any]]] = {}
        for issue in issues:
            assignee = issue.get('assignee') or "Não atribuído"
            developers.setdefault(assignee, []).append(issue)

        # Começa o markdown
        markdown = f"# 📋 Relatório de Desenvolvedores - Milestones e Issues do Repositório {query}\n\n"

        # --- Resumo Geral ---
        markdown += "## 📈 Resumo Geral\n\n"
        markdown += "| Desenvolvedor | Issues Concluídas | Issues Abertas | Total de Issues | % Concluído |\n"
        markdown += "|:--------------|:-----------------:|:--------------:|:---------------:|:-----------:|\n"

        for dev, dev_issues in developers.items():
            total = len(dev_issues)
            closed = sum(1 for i in dev_issues if i.get('state') == 'closed')
            open_ = total - closed
            percent = (closed / total * 100) if total else 0.0
            markdown += f"| {dev} | {closed} | {open_} | {total} | {percent:.1f}% |\n"

        # --- Detalhamento por Desenvolvedor ---
        markdown += "\n## 📋 Detalhamento por Desenvolvedor\n\n"

        for dev, dev_issues in developers.items():
            markdown += f"### 👤 {dev}\n\n"
            markdown += "| Status | Título da Issue | Criada em | Fechada em |\n"
            markdown += "|:------:|:----------------|:---------|:-----------|\n"

            for issue in dev_issues:
                status_emoji = "✅" if issue.get('state') == "closed" else "🚧"
                title = issue.get('title', "Sem título")
                created_at = issue.get('created_at', "-")
                closed_at = issue.get('closed_at') or "-"
                markdown += f"| {status_emoji} | {title} | {created_at} | {closed_at} |\n"

            markdown += "\n"

        return markdown

    def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported.")
