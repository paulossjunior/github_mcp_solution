from typing import List, Dict, Optional, Any
from repository.project_repository import GithHubProjectRepository

class GitHubProjectService():

    def __init__(self):
        self.repository = GithHubProjectRepository()

    def get_all(self, token, login)-> Optional[List[Dict[str, str]]]:

        return self.repository.get_all(token,login) 
    
    def get_projects_milestones_issues (self, token, login)-> Dict[str, List[Dict[str, Any]]]:

        return self.repository.get_projects_milestones_issues(token,login) 