from langchain.tools import BaseTool
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()
class MarkdownGeneratorTool(BaseTool):
    name: str = "generate_markdown_report"
    description: str = "Generates a Markdown report from milestones and issues. Input: {'milestones': [...], 'issues': [...]}."

    def _run(self, data: Dict[str, List[Dict[str, str]]]) -> str:
        milestones = data.get("milestones", [])
        issues = data.get("issues", [])

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

    def _arun(self, data: Dict[str, List[Dict[str, str]]]) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
