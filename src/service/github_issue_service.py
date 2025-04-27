from repository.github_issue_repository import GitHubIssueRepository

class GitHubIssueService():

    def __init__(self):
        self.repository = GitHubIssueRepository()
    
    def get_all (self, repo_path,milestone_number,token):
        return self.repository.get_all(repo_path,milestone_number,token)