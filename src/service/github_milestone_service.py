from repository.github_milestone_repository import GitHubMilestoneRepository

class GitHubMilestoneService():

    def __init__(self):
        self.repository = GitHubMilestoneRepository()
    
    def get_all (self, repo_path, token):
        return self.repository.get_all(repo_path,token)