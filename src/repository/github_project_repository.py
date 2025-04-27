from typing import List, Dict, Optional
import requests

class GithHubProjectRepository():

    # Helper function to run the GraphQL
    def __run_graphql_query(query_text: str, variables:str, token:str) -> Optional[List[Dict[str, str]]]:
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


    def get_all(self,  token,login):

       
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