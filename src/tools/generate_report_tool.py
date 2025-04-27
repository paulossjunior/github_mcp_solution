from langchain.tools import BaseTool
from typing import Any
import json

class GenerateReportTool(BaseTool):
    name: str = "generate_full_markdown_report"
    description: str = "Generates a Markdown report based on previously saved milestones and issues in memory."

    def _run(self, chat_history: Any) -> str:
        milestones = []
        issues = []

        for message in chat_history:
            content = message
            if hasattr(message, "content"):
                content = message.content

            # 🛠️ SE for string, tentar fazer JSON decode
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except Exception:
                    continue  # Se não conseguir, ignora

            if isinstance(content, dict):
                if "milestones" in content and "issues" in content:
                    milestones = content["milestones"]
                    issues = content["issues"]
            elif isinstance(content, list) and content and isinstance(content[0], dict):
                if "number" in content[0] and "title" in content[0]:
                    milestones = content
                if "creator" in content[0] and "assignee" in content[0]:
                    issues = content

        if not milestones:
            return "Desculpe, não foi possível gerar o relatório em Markdown pois nenhum milestone foi encontrado. Parece que houve um problema ao salvar os milestones e issues na memória."

        markdown = "# 📋 Relatório de Milestones e Issues\n\n"

        for m in milestones:
            markdown += f"## 📌 Milestone {m['number']} - {m['title']}\n"
            markdown += f"- Criado em: {m['created_at']}\n"
            markdown += f"- Entrega prevista: {m['due_on']}\n"
            markdown += f"- Estado: {m['state']}\n\n"

            milestone_issues = [i for i in issues if i.get("milestone_number") == m["number"]]

            if milestone_issues:
                markdown += "| Status | Título | Criado por | Atribuído para | Criada em | Fechada em |\n"
                markdown += "|:------:|:-------|:-----------|:---------------|:---------|:-----------|\n"

                for i in milestone_issues:
                    status_emoji = "✅" if i['state'] == "closed" else "🚧"
                    closed_at = i['closed_at'] if i['closed_at'] else "-"
                    markdown += f"| {status_emoji} | {i['title']} | {i['creator']} | {i['assignee']} | {i['created_at']} | {closed_at} |\n"

                markdown += "\n"
            else:
                markdown += "Nenhuma issue para este milestone.\n\n"

        return markdown

    def _arun(self, chat_history: Any) -> str:
        raise NotImplementedError("Async not supported.")
