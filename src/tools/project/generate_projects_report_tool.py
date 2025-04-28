from typing import Optional
from langchain.tools import BaseTool
from .list_projects_cards_milestones_tool import ListProjectsCardsMilestonesTool
from service.github_project_service import GitHubProjectService
class GenerateProjectsReportTool(BaseTool):
    name: str = "generate_projects_full_markdown_report"
    description: str = (
        "Generates a complete Markdown report with projects, repositories, milestones, and issues, "
        "including summaries per project."
    )

    def _run(self, organization: str) -> str:
        
        list_tool = ListProjectsCardsMilestonesTool()
        service = GitHubProjectService()   
        projects_data = list_tool._run(organization)
        return service.generate_projects_full_markdown_report(projects_data=projects_data,
                                                              organization=organization
                                                              )
        
    def _arun(self, organization: str) -> Optional[str]:
        raise NotImplementedError("Async not supported.")
