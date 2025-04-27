import os
import requests
from typing import List, Dict, Any, Optional
from langchain.tools import BaseTool

class ListProjectsCardsMilestonesTool(BaseTool):
    name: str = "list_projects_cards_milestones"
    description: str = (
        "Fetches all GitHub Projects V2, repositories, milestones, and issues (with developers) for a given organization.\n"
        "Input: GitHub organization login."
    )

    def _run(self, organization: str) -> Dict[str, List[Dict[str, Any]]]:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN não encontrado nas variáveis de ambiente.")

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        organization = organization.strip().replace("`", "").replace("\n", "")

        # GraphQL para listar projetos
        org_projects_query = """
        query($login: String!) {
          organization(login: $login) {
            projectsV2(first: 50) {
              nodes {
                id
                title
                number
                createdAt
                updatedAt
                url
              }
            }
          }
        }
        """

        # GraphQL para repositórios associados a projeto
        project_repositories_query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              repositories(first: 20) {
                nodes {
                  name
                  url
                }
              }
            }
          }
        }
        """

        # GraphQL para milestones e issues (agora com criador e assignee)
        repo_milestones_query = """
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            milestones(first: 20) {
              nodes {
                number
                title
                description
                dueOn
                state
                createdAt
                updatedAt
                issues(first: 50) {
                  nodes {
                    number
                    title
                    state
                    createdAt
                    closedAt
                    url
                    creator {
                      login
                    }
                    assignees(first: 5) {
                      nodes {
                        login
                      }
                    }
                  }
                }
              }
            }
          }
        }
        """

        # Função auxiliar para rodar queries
        def run_query(query_text: str, variables: Dict[str, Any]) -> Dict[str, Any]:
            response = requests.post(
                "https://api.github.com/graphql",
                headers=headers,
                json={"query": query_text, "variables": variables},
                timeout=15
            )
            response.raise_for_status()
            return response.json()

        # Buscar projetos
        projects_data = run_query(org_projects_query, {"login": organization})
        org_projects = projects_data.get("data", {}).get("organization", {}).get("projectsV2", {}).get("nodes", [])

        if not org_projects:
            raise ValueError(f"Nenhum projeto encontrado para a organização '{organization}'.")

        result = []
        for project in org_projects:
            project_entry = {
                "id": project.get("id"),
                "title": project.get("title"),
                "number": project.get("number"),
                "created_at": project.get("createdAt"),
                "updated_at": project.get("updatedAt"),
                "url": project.get("url"),
                "repositories": []
            }

            # Buscar repositórios
            repos_data = run_query(project_repositories_query, {"projectId": project["id"]})
            repositories = repos_data.get("data", {}).get("node", {}).get("repositories", {}).get("nodes", [])

            for repo in repositories:
                repo_name = repo.get("name")
                repo_url = repo.get("url")
                repo_entry = {
                    "name": repo_name,
                    "url": repo_url,
                    "milestones": []
                }

                # Buscar milestones e issues (com devs)
                try:
                    repo_milestone_data = run_query(repo_milestones_query, {"owner": organization, "repo": repo_name})
                    milestones = repo_milestone_data.get("data", {}).get("repository", {}).get("milestones", {}).get("nodes", [])
                except Exception:
                    milestones = []

                for milestone in milestones:
                    milestone_entry = {
                        "number": milestone.get("number"),
                        "title": milestone.get("title"),
                        "description": milestone.get("description"),
                        "dueOn": milestone.get("dueOn"),
                        "state": milestone.get("state"),
                        "createdAt": milestone.get("createdAt"),
                        "updatedAt": milestone.get("updatedAt"),
                        "issues": []
                    }

                    issues = milestone.get("issues", {}).get("nodes", [])
                    for issue in issues:
                        milestone_entry["issues"].append({
                            "number": issue.get("number"),
                            "title": issue.get("title"),
                            "state": issue.get("state"),
                            "createdAt": issue.get("createdAt"),
                            "closedAt": issue.get("closedAt"),
                            "url": issue.get("url"),
                            "creator": issue.get("creator", {}).get("login", "Desconhecido"),
                            "assignees": [assignee.get("login", "Desconhecido") for assignee in issue.get("assignees", {}).get("nodes", [])]
                        })

                    repo_entry["milestones"].append(milestone_entry)

                project_entry["repositories"].append(repo_entry)

            result.append(project_entry)

        return {"projects": result}

    def _arun(self, organization: str) -> Dict[str, List[Dict[str, Any]]]:
        raise NotImplementedError("Async not supported.")
