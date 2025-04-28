from typing import List, Dict, Any

class GitHubRepositoryService():

    def generate_developer_markdown_report(self, issues:List, repository:str)-> str:
        
         # Agrupar issues por assignee
        developers: Dict[str, List[Dict[str, Any]]] = {}
        for issue in issues:
            assignee = issue.get('assignee') or "Não atribuído"
            developers.setdefault(assignee, []).append(issue)

        # Começa o markdown
        markdown = f"# 📋 Relatório de Desenvolvedores - Milestones e Issues do Repositório {repository}\n\n"

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


    def generate_milestone_issue_markdown_report(self, milestones:List , issues:List, repository:str)-> str:
        
        # Começa relatório
        markdown = f"# 📋 Relatório de Milestones e Issues do Repositório {repository}\n\n"

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
