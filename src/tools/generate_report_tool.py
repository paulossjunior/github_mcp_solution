from langchain.tools import BaseTool
from typing import Dict, Any
import json
from dotenv import load_dotenv

load_dotenv()

class GenerateReportTool(BaseTool):
    name: str = "generate_full_markdown_report"
    description: str = "Generates a Markdown report based on previously saved milestones and issues in memory."

    def _run(self, chat_history: Any) -> str:
        milestones = []
        issues = []

        for message in chat_history:
            content = message.content
            if content.startswith("milestones:"):
                try:
                    milestones_data = content.replace("milestones:", "").strip()
                    milestones = json.loads(milestones_data.replace("'", '"'))
                except Exception as e:
                    print(f"Erro carregando milestones: {e}")
            if content.startswith("issues:"):
                try:
                    issues_data = content.replace("issues:", "").strip()
                    issues = json.loads(issues_data.replace("'", '"'))
                except Exception as e:
                    print(f"Erro carregando issues: {e}")

        if not milestones:
            return "Nenhum milestone encontrado para gerar relatório."

        # Gerar Markdown na mão (igual MarkdownGenerator)
        markdown = "# 📋 Relatório de Milestones e Issues\n\n"

        for m in milestones:
            markdown += f"## 📌 {m['title']}\n"
            markdown += f"- Criado em: {m['created_at']}\n"
            markdown += f"- Entrega prevista: {m['due_on']}\n"
            markdown += f"- Estado: {m['state']}\n\n"

        if issues:
            markdown += "# 📋 Issues Relacionadas\n\n"
            for i in issues:
                markdown += f"- {i['title']} ({i['state']}) - Criado em {i['created_at']}\n"
        else:
            markdown += "Nenhuma issue encontrada.\n"

        return markdown

    def _arun(self, chat_history: Any) -> str:
        raise NotImplementedError("Async not supported.")
