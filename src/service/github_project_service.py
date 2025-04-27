from typing import List, Dict, Optional
from repository.project_repository import GithHubProjectRepository

class GitHubProjectService():

    def __init__(self):
        self.repository = GithHubProjectRepository()

    def get_all(self, token, login)-> Optional[List[Dict[str, str]]]:

        return self.repository.get_all(token,login) 