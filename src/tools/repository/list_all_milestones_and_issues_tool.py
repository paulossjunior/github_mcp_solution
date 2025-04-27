from typing import List, Dict, Any
from langchain.tools import BaseTool
from .github_milestones_tool import GitHubMilestoneTool
from .github_issue_tool import GitHubIssueTool

class ListAllMilestonesAndIssuesTool(BaseTool):
    name: str = "list_all_milestones_and_issues"
    description: str = (
        "Fetches all milestones and issues from a GitHub repository. "
        "Input: 'owner/repo'. Automatically collects milestones and their related issues."
    )

    def _run(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        # Limpeza do input
        repo_path = query
        if isinstance(repo_path, list):
            repo_path = repo_path[0]
        repo_path = repo_path.replace("`", "").replace("\n", "").strip()

        # Validação básica
        if "/" not in repo_path:
            raise ValueError(f"Formato inválido: '{repo_path}'. Esperado 'owner/repo'.")

        # Usar GitHubRepositoryTool para obter milestones
        repo_tool = GitHubMilestoneTool()
        milestones = repo_tool._run(repo_path)

        # Usar GitHubIssueTool para obter issues de cada milestone
        issue_tool = GitHubIssueTool()

        all_issues: List[Dict[str, Any]] = []
        
        for milestone in milestones:
            number = milestone.get("number")
            if number is None:
                continue
            # Monta input para issues: 'owner/repo/number'
            issue_input = f"{repo_path}/{number}"
            issues = issue_tool._run(issue_input)
            # Adiciona metadata do milestone em cada issue
            for issue in issues:
                issue["milestone_number"] = number
                issue["milestone_title"] = milestone.get("title")
                all_issues.append(issue)

        return {
            "milestones": milestones,
            "issues": all_issues
        }

    def _arun(self, query: str) -> Dict[str, List[Dict[str, Any]]]:
        raise NotImplementedError("Async not supported.")
