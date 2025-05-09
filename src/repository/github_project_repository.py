from typing import List, Dict, Optional, Any
import requests

class GithHubProjectRepository():

    # Helper function to run the GraphQL
    def __run_graphql_query(self, query_text: str, variables:str, token:str) -> Optional[List[Dict[str, str]]]:
        try:
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json"
            }

            response = requests.post(
                    "https://api.github.com/graphql",
                    headers=headers,
                    json={"query": query_text, "variables": variables},
                    timeout=15
            )
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
                raise RuntimeError(f"Request failed: {e}")


    def get_all(self, token,login):

       
        # Define separate queries
        user_query = """
        query($login: String!) {
          user(login: $login) {
            projectsV2(first: 100) {
              nodes {
                id
                title
                number
                createdAt
                updatedAt
                closed
                public
                url
              }
            }
          }
        }
        """

        org_query = """
        query($login: String!) {
          organization(login: $login) {
            projectsV2(first: 100) {
              nodes {
                id
                title
                number
                createdAt
                updatedAt
                closed
                public
                url
              }
            }
          }
        }
        """

        variables = {"login": login}

        data = self.__run_graphql_query(user_query,variables,token)

        if "errors" in data and any(err.get("type") == "NOT_FOUND" for err in data["errors"]):
            # Try as organization
            data = self.__run_graphql_query(org_query,variables,token)

        if "errors" in data:
            raise ValueError(f"GitHub API error: {data['errors']}")

        # Extract projects from the correct field
        user_projects = data.get("data", {}).get("user", {}).get("projectsV2", {}).get("nodes", [])
        org_projects = data.get("data", {}).get("organization", {}).get("projectsV2", {}).get("nodes", [])
        projects = user_projects or org_projects or []

        if not projects:
            raise ValueError(f"No projects found for '{login}'.")
        
        return [
            {
                "id": project.get("id"),
                "number": project.get("number"),
                "title": project.get("title"),
                "created_at": project.get("createdAt"),
                "updated_at": project.get("updatedAt"),
                "closed": project.get("closed"),
                "public": project.get("public"),
                "url": project.get("url")
            }
            for project in projects if project
        ]
    

    def get_project_repository (self, token, login)-> Optional[List[Dict[str, str]]]:
         # GraphQL para repositórios associados a projeto
        query = """
        query($projectId: ID!) {
          node(id: $projectId) {
            ... on ProjectV2 {
              repositories(first: 100) {
                nodes {
                  name
                  url
                }
              }
            }
          }
        }
        """
        data = self.__run_graphql_query(query, login, token)

        repositories = data.get("data", {}).get("node", {}).get("repositories", {}).get("nodes", [])
        result = []
        for repo in repositories:
          repo_entry = {
                "name": repo.get("name"),
                "url": repo.get("url"),
                "milestones": []
            }
          result.append (repo_entry)
        return result
    
    def get_project_milestone_issue (self, token, login)-> Optional[List[Dict[str, str]]]:
        # GraphQL para milestones e issues (agora com criador e assignee)
        query = """
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            milestones(first: 100) {
              nodes {
                number
                title
                description
                dueOn
                state
                createdAt
                updatedAt
                issues(first: 100) {
                  nodes {
                    number
                    title
                    state
                    createdAt
                    closedAt
                    url
                    author {
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

        data = self.__run_graphql_query(query, login, token)
        try:
          milestones = data.get("data", {}).get("repository", {}).get("milestones", {}).get("nodes", [])
          result = []
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
                  "author": issue.get("author", {}).get("login", "Desconhecido"),
                  "assignees": [assignee.get("login", "Desconhecido") for assignee in issue.get("assignees", {}).get("nodes", [])]
                })
              result.append(milestone_entry)

          
        except Exception:
          result = []

        return result
    

    def get_projects_milestones_issues(self,token, login) -> Dict[str, List[Dict[str, Any]]]:
         
        
        projects_data = self.get_all(token=token, login=login)
        if not projects_data:
            raise ValueError(f"Nenhum projeto encontrado para a organização '{login}'.")

        result = []

        for project in projects_data:
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
            repositories = self.get_project_repository(token=token,login={"projectId": project["id"]})
            project_entry["repositories"].extend(repositories)

            for repository in repositories:
              milestones =  self.get_project_milestone_issue(token=token,login={"owner": login, "repo": repository['name']})
              repository["milestones"].extend(milestones)
            
            
            result.append(project_entry)
          
        return result
