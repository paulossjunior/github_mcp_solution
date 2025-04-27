import os
import requests
from langchain.tools import BaseTool
from typing import List, Dict, Optional

class GitHubProjectsV2Tool(BaseTool):
    name: str = "list_github_projects_v2"
    description: str = (
        "Fetches all GitHub Projects V2 for a given organization or user.\n"
        "Input: GitHub organization or user login."
    )

    def _run(self, login: str) -> List[Dict[str, str]]:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN environment variable not set.")

        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json"
        }

        login = login.strip().replace("`", "").replace("\n", "")

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

        # Helper function to run the GraphQL
        def run_graphql_query(query_text: str) -> Optional[List[Dict[str, str]]]:
            try:
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

        # Try as user first
        data = run_graphql_query(user_query)

        if "errors" in data and any(err.get("type") == "NOT_FOUND" for err in data["errors"]):
            # Try as organization
            data = run_graphql_query(org_query)

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

    def _arun(self, login: str) -> Optional[List[Dict[str, str]]]:
        raise NotImplementedError("Async not supported.")
