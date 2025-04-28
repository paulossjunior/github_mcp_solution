import pytest
import os
from src.service.github_project_service import GitHubProjectService
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture(scope="module")
def data_test():
    token = os.getenv("GITHUB_TOKEN")
    login = "leds-conectafapes"
    return  {
        "token": token,
        "login": login
    }

@pytest.fixture(scope="module")
def repo():
    return  GitHubProjectService()

def test_get_all(repo, data_test):
    
    token = data_test["token"]
    login = data_test["login"]

    result = repo.get_all(token=token, login=login)
    assert result is not None and len(result) > 0

def test_get_projects_milestones_issues(repo, data_test):
    
    token = data_test["token"]
    login = data_test["login"]

    result = repo.get_projects_milestones_issues(token=token, login=login)
    assert result is not None and len(result) > 0


def test_generate_projects_full_markdown_report(repo, data_test):
    
    token = data_test["token"]
    login = data_test["login"]
    
    projects = repo.get_all(token=token, login=login)
    assert projects is not None and len(projects) > 0
    
    data = {"projects": projects}
    result = repo.generate_projects_full_markdown_report(projects_data=data, organization=login)
    
    assert result is not None and len(result) > 0