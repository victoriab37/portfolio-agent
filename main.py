"""
Portfolio Agent - AI-powered project idea generator & article drafter
Run: python main.py
"""

import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from agents.orchestrator import OrchestratorAgent

load_dotenv()
console = Console()


def main():
    console.print(Panel.fit(
        "[bold purple]Portfolio Agent[/bold purple]\n"
        "[dim]AI-powered project ideas + Medium article drafts[/dim]",
        border_style="purple"
    ))

    profile = {
        "name": "Victoria",
        "role": "Frontend Software Engineer",
        "years_experience": 3,
        "skills": [
            "Python", "TypeScript", "JavaScript", "Java",
            "Angular", "React", "Node.js",
            "AWS (IAM, S3, EC2, Lambda, CloudTrail)",
            "Splunk", "GuardDuty", "Dynatrace", "Datadog",
            "GitLab CI/CD", "Linux CLI", "DevSecOps"
        ],
        "certifications": [
            "CompTIA Security+ (SY0-701)",
            "AWS Certified Cloud Practitioner",
            "Certified Scrum Master"
        ],
        "target_roles": ["AI Engineer", "Security Engineer", "Cloud Security Engineer"],
        "existing_projects": ["Cloud Log Monitoring & Alerting System (Mini SIEM)"],
        "blog": "https://medium.com/@victoriab37",
        "github": "https://github.com/victoriab37"
    }

    orchestrator = OrchestratorAgent(profile)

    console.print("\n[bold]Step 1:[/bold] Researching current trends in AI & security roles...")
    trends = orchestrator.research_trends()

    console.print("\n[bold]Step 2:[/bold] Generating project ideas tailored to your profile...")
    ideas = orchestrator.generate_ideas(trends)

    console.print("\n[bold]Step 3:[/bold] Evaluating and ranking ideas...")
    ranked = orchestrator.evaluate_ideas(ideas)

    console.print("\n[bold green]Top project ideas for you:[/bold green]")
    for i, idea in enumerate(ranked, 1):
        console.print(Panel(
            f"[bold]{idea['title']}[/bold]\n\n"
            f"[dim]Stack:[/dim] {idea['stack']}\n"
            f"[dim]Why it fits:[/dim] {idea['why_it_fits']}\n"
            f"[dim]Score:[/dim] {idea['score']}/10",
            title=f"#{i}",
            border_style="green"
        ))

    console.print("\nWhich project do you want to develop? (enter number)")
    choice = int(input("> ")) - 1
    chosen = ranked[choice]

    if Confirm.ask(f"\nGenerate a Medium article draft for [bold]{chosen['title']}[/bold]?"):
        console.print("\n[bold]Step 4:[/bold] Writing your Medium article draft...")
        article = orchestrator.write_article(chosen)

        console.print("\n[bold]Step 5:[/bold] Generating GitHub README...")
        readme = orchestrator.write_readme(chosen)

        os.makedirs("output", exist_ok=True)
        safe_title = chosen['title'].lower().replace(" ", "-")[:40]

        with open(f"output/{safe_title}-article.md", "w") as f:
            f.write(article)
        with open(f"output/{safe_title}-README.md", "w") as f:
            f.write(readme)

        console.print(Panel.fit(
            f"[bold green]Done![/bold green]\n\n"
            f"[dim]Article draft:[/dim] output/{safe_title}-article.md\n"
            f"[dim]README:[/dim] output/{safe_title}-README.md",
            border_style="green"
        ))

        if Confirm.ask("\nCreate a GitHub repo for this project?"):
            orchestrator.create_github_repo(chosen, readme)


if __name__ == "__main__":
    main()
