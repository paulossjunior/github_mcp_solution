import pytest
import os
from src.service.github_milestone_service import GitHubMilestoneService
from src.service.github_issue_service import GitHubIssueService
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture(scope="module")
def data_test():
    token = os.getenv("GITHUB_TOKEN")
    repo_path = "leds-conectafapes/conectafapes-planning"
    return  {
        "token": token,
        "repo_path": repo_path
    }

@pytest.fixture(scope="module")
def repo():
    return  GitHubMilestoneService()
       

@pytest.fixture(scope="module")
def repo_issue():
    return  GitHubIssueService()


def test_get_all(repo, repo_issue, data_test):
    token = data_test["token"]
    repo_path = data_test["repo_path"]
    
    milestones = repo.get_all(repo_path, token=token)
    assert milestones is not None and len(milestones) > 0
    result = []
    
    for milestone in milestones:
        issues = repo_issue.get_all(repo_path, milestone["number"], token=token)
        result.extend (issues)

    assert result is not None and len(result) > 0

