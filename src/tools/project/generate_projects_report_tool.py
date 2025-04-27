from typing import Optional
from langchain.tools import BaseTool
from .list_projects_cards_milestones_tool import ListProjectsCardsMilestonesTool

class GenerateProjectsReportTool(BaseTool):
    name: str = "generate_projects_full_markdown_report"
    description: str = (
        "Generates a complete Markdown report with projects, repositories, milestones, and issues, "
        "including summaries per project."
    )

    def _run(self, organization: str) -> str:
        list_tool = ListProjectsCardsMilestonesTool()
        projects_data = list_tool._run(organization)

        if not isinstance(projects_data, dict) or "projects" not in projects_data:
            raise ValueError("Erro ao processar dados recebidos.")

        markdown = f"# 📋 Relatório Completo de Projetos - Organização: `{organization}`\n\n"

        for project in projects_data["projects"]:
            markdown += f"## 🚀 Projeto: {project['title']}\n"
            markdown += f"- **ID**: {project['id']}\n"
            markdown += f"- **Número**: {project['number']}\n"
            markdown += f"- **Criado em**: {project.get('created_at', 'N/A')}\n"
            markdown += f"- **Atualizado em**: {project.get('updated_at', 'N/A')}\n"
            markdown += f"- **URL**: [{project['url']}]({project['url']})\n\n"

            if not project.get("repositories"):
                markdown += "⚠️ Nenhum repositório associado a este projeto.\n\n"
                continue

            # RESUMO por projeto: Milestones
            markdown += "### 📊 Resumo de Milestones\n\n"
            markdown += "| Milestone | Issues Concluídas | Issues Abertas | Total | % Concluído |\n"
            markdown += "|:----------|:-----------------:|:--------------:|:-----:|:-----------:|\n"

            milestone_summaries = []

            for repo in project["repositories"]:
                for milestone in repo.get("milestones", []):
                    issues = milestone.get("issues", [])
                    closed = sum(1 for issue in issues if issue["state"] == "closed")
                    open_ = len(issues) - closed
                    total = len(issues)
                    percent = (closed / total) * 100 if total > 0 else 0
                    milestone_summaries.append({
                        "title": milestone["title"],
                        "closed": closed,
                        "open": open_,
                        "total": total,
                        "percent": f"{percent:.1f}%"
                    })

            if milestone_summaries:
                for m in milestone_summaries:
                    markdown += f"| {m['title']} | {m['closed']} | {m['open']} | {m['total']} | {m['percent']} |\n"
            else:
                markdown += "| Nenhum milestone encontrado | - | - | - | - |\n"

            markdown += "\n"

            # DETALHAMENTO
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

                    markdown += "| Status | Título da Issue | Criador | Responsáveis | Criada em | Fechada em | URL |\n"
                    markdown += "|:------:|:----------------|:--------|:------------|:---------|:-----------|:----|\n"

                    for issue in milestone["issues"]:
                        status_emoji = "✅" if issue["state"] == "closed" else "🚧"
                        closed_at = issue.get("closedAt", "-")
                        creator = issue.get("creator", "Desconhecido")
                        assignees = issue.get("assignees", [])
                        assignees_str = ", ".join(assignees) if assignees else "Não atribuído"
                        markdown += (
                            f"| {status_emoji} | {issue['title']} | {creator} | {assignees_str} | "
                            f"{issue['createdAt']} | {closed_at} | [Link]({issue['url']}) |\n"
                        )

                    markdown += "\n"

        return markdown

    def _arun(self, organization: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
