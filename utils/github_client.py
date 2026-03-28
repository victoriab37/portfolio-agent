"""
GitHub client — creates repos using PyGithub.
"""

import os
from github import Github


class GitHubClient:
    def __init__(self):
        token = os.getenv("GITHUB_TOKEN")
        self.gh = Github(token) if token else None

    def create_repo(self, name: str, description: str, readme_content: str) -> str:
        if not self.gh:
            raise ValueError("GITHUB_TOKEN not set.")
        user = self.gh.get_user()
        repo = user.create_repo(
            name=name,
            description=description,
            private=False,
            auto_init=False,
        )
        repo.create_file(
            "README.md",
            "Initial commit — scaffolded by Portfolio Agent",
            readme_content,
        )
        return repo.html_url
