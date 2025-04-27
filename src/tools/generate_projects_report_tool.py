import os
from typing import Optional
from langchain.tools import BaseTool
from .list_projects_cards_milestones_tool import ListProjectsCardsMilestonesTool

class GenerateProjectsReportTool(BaseTool):
    name: str = "generate_projects_full_markdown_report"
    description: str = (
        "Generates a complete Markdown report of all GitHub Projects V2, including associated repositories, milestones, and issues. "
        "Input: GitHub organization or user login."
    )

    def _run(self, query: str) -> str:
        # Usa a ferramenta de listar projetos
        list_tool = ListProjectsCardsMilestonesTool()
        data = list_tool._run(query)

        # Agora acessa corretamente
        projects_data = data.get("projects", [])

        if not isinstance(projects_data, list):
            raise ValueError("Erro ao processar dados recebidos.")

        markdown = f"# 📋 Relatório Completo de Projetos - Organização: `{query}`\n\n"

        for project in projects_data:
            markdown += f"## 🚀 Projeto: {project['title']}\n"
            markdown += f"- **ID**: {project['id']}\n"
            markdown += f"- **Número**: {project['number']}\n"
            markdown += f"- **Criado em**: {project.get('created_at', 'N/A')}\n"
            markdown += f"- **Atualizado em**: {project.get('updated_at', 'N/A')}\n"
            markdown += f"- **URL**: [{project['url']}]({project['url']})\n\n"

            if not project.get("repositories"):
                markdown += "⚠️ Nenhum repositório associado a este projeto.\n\n"
                continue

            for repo in project["repositories"]:
                markdown += f"### 📦 Repositório: {repo['name']}\n"
                markdown += f"- **URL**: [{repo['url']}]({repo['url']})\n\n"

                if not repo.get("milestones"):
                    markdown += "⚠️ Nenhum milestone encontrado neste repositório.\n\n"
                    continue

                for milestone in repo["milestones"]:
                    markdown += f"#### 🏁 Milestone: {milestone['title']} ({milestone['state']})\n"
                    markdown += f"- **Criado em**: {milestone.get('createdAt', 'N/A')}\n"
                    markdown += f"- **Entrega prevista**: {milestone.get('dueOn', 'N/A')}\n\n"

                    if not milestone.get("issues"):
                        markdown += "⚠️ Nenhuma issue associada a este milestone.\n\n"
                        continue

                    markdown += "| Status | Título da Issue | Criada em | Fechada em | URL |\n"
                    markdown += "|:------:|:----------------|:---------|:-----------|:----|\n"

                    for issue in milestone["issues"]:
                        status_emoji = "✅" if issue['state'] == "closed" else "🚧"
                        closed_at = issue.get("closedAt", "-")
                        markdown += (
                            f"| {status_emoji} | {issue['title']} | {issue['createdAt']} | {closed_at} | "
                            f"[Link]({issue['url']}) |\n"
                        )

                    markdown += "\n"

        return markdown


    def _arun(self, query: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
