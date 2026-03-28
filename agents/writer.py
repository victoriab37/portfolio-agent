"""
Writer agent — drafts Medium articles and GitHub READMEs using Claude.
"""

import os
import anthropic


class WriterAgent:
    def __init__(self, profile: dict):
        self.profile = profile
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def draft_article(self, project: dict) -> str:
        system_prompt = f"""You are a technical writer helping {self.profile['name']}, a {self.profile['role']},
write a Medium blog post in first person. Write in a clear, personal, practitioner voice —
not academic, not marketing. The tone is: "here's what I built, here's what I learned."

The author's background: {', '.join(self.profile['skills'][:6])}.
Their certifications: {', '.join(self.profile['certifications'])}.
Their GitHub: {self.profile['github']}
Their blog: {self.profile['blog']}

Structure the article as:
1. Hook (why this matters, 1-2 paragraphs)
2. What I built (project overview)
3. Architecture / how it works (with code concepts, not full code)
4. Key challenges and how I solved them
5. What I learned
6. What's next
7. Closing + links

Use markdown formatting. Aim for 800-1200 words. Write as Victoria in first person."""

        user_prompt = f"""Write a Medium article for this project:

Title: {project['title']}
Description: {project.get('description', '')}
Stack: {project.get('stack', '')}
Learning goals: {', '.join(project.get('learning_goals', []))}
Why it fits my background: {project.get('why_it_fits', '')}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text

    def draft_readme(self, project: dict) -> str:
        system_prompt = f"""You are writing a professional GitHub README for {self.profile['name']}'s portfolio project.
Make it impressive for hiring managers at AI and security companies.
Include: project badges placeholder, description, architecture overview, setup instructions,
usage, key concepts learned, and a link to the Medium article at {self.profile['blog']}.
Use markdown. Keep it concise but complete."""

        user_prompt = f"""Write a README for:

Title: {project['title']}
Description: {project.get('description', '')}
Stack: {project.get('stack', '')}
Learning goals: {', '.join(project.get('learning_goals', []))}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        return response.content[0].text
