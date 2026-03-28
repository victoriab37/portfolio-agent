"""
Orchestrator agent — coordinates all sub-agents and manages the pipeline.
"""

import os
from rich.console import Console
from agents.researcher import ResearchAgent
from agents.ideator import IdeatorAgent
from agents.evaluator import EvaluatorAgent
from agents.writer import WriterAgent
from utils.github_client import GitHubClient

console = Console()


class OrchestratorAgent:
    def __init__(self, profile: dict):
        self.profile = profile
        self.researcher = ResearchAgent()
        self.ideator = IdeatorAgent(profile)
        self.evaluator = EvaluatorAgent(profile)
        self.writer = WriterAgent(profile)
        self.github = GitHubClient()

    def research_trends(self) -> dict:
        queries = [
            f"top skills for {role} jobs 2025" for role in self.profile["target_roles"]
        ]
        queries.append("trending AI security GitHub projects 2025")
        queries.append("LLM cybersecurity portfolio projects 2025")

        results = {}
        for query in queries:
            console.print(f"  [dim]Searching:[/dim] {query}")
            results[query] = self.researcher.search(query)
        return results

    def generate_ideas(self, trends: dict) -> list:
        trend_summary = "\n".join(
            f"- {k}: {v[:300]}" for k, v in trends.items() if v
        )
        return self.ideator.generate(trend_summary)

    def evaluate_ideas(self, ideas: list) -> list:
        return self.evaluator.rank(ideas)

    def write_article(self, project: dict) -> str:
        return self.writer.draft_article(project)

    def write_readme(self, project: dict) -> str:
        return self.writer.draft_readme(project)

    def create_github_repo(self, project: dict, readme: str):
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            console.print("[yellow]GITHUB_TOKEN not set — skipping repo creation.[/yellow]")
            return
        repo_name = project["title"].lower().replace(" ", "-").replace("/", "-")[:40]
        description = project.get("why_it_fits", "AI/Security portfolio project")
        try:
            url = self.github.create_repo(repo_name, description, readme)
            console.print(f"\n[bold green]Repo created:[/bold green] {url}")
        except Exception as e:
            console.print(f"[red]GitHub error:[/red] {e}")
