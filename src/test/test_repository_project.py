import pytest
import os
from src.repository.github_project_repository import GithHubProjectRepository
from dotenv import load_dotenv


load_dotenv()

@pytest.fixture(scope="module")
def data_test():
    repo = GithHubProjectRepository()
    token = os.getenv("GITHUB_TOKEN")
    login = "leds-conectafapes"
    return  {
        "token": token,
        "login": login
    }

@pytest.fixture(scope="module")
def repo():
    return  GithHubProjectRepository()
       

def test_get_all_project(repo, data_test):
    token = data_test["token"]
    login = data_test["login"]
    
    result = repo.get_all(token=token,login=login)
    assert result is not None and len(result) > 0

def test_get_all_project_repository(repo,data_test):

    token = data_test["token"]
    login = data_test["login"]
    
    projects = repo.get_all(token=token,login=login)
    assert projects is not None and len(projects) > 0
    result = []

    for project in projects:
        repositories = repo.get_project_repository(token=token,login={"projectId": project["id"]})
        print (f'project: {project['title']}')
        print ("repositorios")
        print (repositories)
        result.append(repositories)

    assert result is not None and len(result) > 0

def test_get_all_milestone_respository(repo, data_test):

    token = data_test["token"]
    login = data_test["login"]
    
    projects = repo.get_all(token=token,login=login)
    assert projects is not None and len(projects) > 0
    result = []

    for project in projects:
        repositories = repo.get_project_repository(token=token,login={"projectId": project["id"]})
        for repository in repositories:
            milestones = repo.get_project_milestone_issue(token=token,login={"owner": login, "repo": repository["name"]}) 
            print (milestones)
            result.append(milestones)

    assert result is not None and len(result) > 0
