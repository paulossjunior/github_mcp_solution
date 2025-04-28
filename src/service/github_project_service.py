from typing import List, Dict, Optional, Any
from repository.github_project_repository import GithHubProjectRepository

class GitHubProjectService():

    def __init__(self):
        self.repository = GithHubProjectRepository()

    def get_all(self, token, login)-> Optional[List[Dict[str, str]]]:

        return self.repository.get_all(token,login) 
    
    def get_projects_milestones_issues (self, token, login)-> Dict[str, List[Dict[str, Any]]]:

        return self.repository.get_projects_milestones_issues(token,login) 
    
    def generate_projects_full_markdown_report (self, projects_data: dict, organization: str)->str:

        if not isinstance(projects_data, dict) or "projects" not in projects_data:
            raise ValueError("Erro ao processar dados recebidos.")

        markdown = f"# 📋 Relatório Completo de Projetos - Organização: `{organization}`\n\n"

        for project in projects_data["projects"]:
            markdown += f"## 🚀 Projeto: {project['title']}\n"
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
                    closed = sum(1 for issue in issues if issue["closedAt"])
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
                        closed_at = issue.get("closedAt")
                        status_emoji = "✅" if closed_at else "🚧"
                        closed_at = closed_at or "-"
                        author = issue.get("author", {}).get("login", "Desconhecido")
                        assignees = issue.get("assignees", [])
                        assignees_str = ", ".join(assignees) if assignees else "Não atribuído"
                        markdown += (
                            f"| {status_emoji} | {issue['title']} | {author} | {assignees_str} | "
                            f"{issue['createdAt']} | {closed_at} | [Link]({issue['url']}) |\n"
                        )

                    markdown += "\n"

        return markdown