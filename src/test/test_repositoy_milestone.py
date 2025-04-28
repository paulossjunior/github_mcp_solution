import pytest
import os
from src.repository.github_milestone_repository import GitHubMilestoneRepository
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
    return  GitHubMilestoneRepository()
       

def test_get_all(repo, data_test):
    token = data_test["token"]
    repo_path = data_test["repo_path"]
    
    result = repo.get_all(repo_path, token=token)
    assert result is not None and len(result) > 0

