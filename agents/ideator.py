"""
Ideator agent — generates tailored portfolio project ideas using Claude.
"""

import os
import json
import anthropic


class IdeatorAgent:
    def __init__(self, profile: dict):
        self.profile = profile
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, trend_summary: str) -> list:
        system_prompt = f"""You are a senior tech career advisor specializing in AI and cybersecurity.
You generate portfolio project ideas tailored to a specific engineer's background.

Engineer profile:
- Name: {self.profile['name']}
- Role: {self.profile['role']} ({self.profile['years_experience']} years)
- Skills: {', '.join(self.profile['skills'])}
- Certifications: {', '.join(self.profile['certifications'])}
- Target roles: {', '.join(self.profile['target_roles'])}
- Existing projects: {', '.join(self.profile['existing_projects'])}

Generate ideas that:
1. Build on their existing skills (don't start from zero)
2. Are achievable solo in 1-3 weeks
3. Are impressive for their target roles
4. Are distinct from their existing projects
5. Combine AI + security where possible (their unique angle)

Respond ONLY with a valid JSON array. No markdown, no preamble.
Each item must have: title, description, stack, learning_goals (array), why_it_fits"""

        user_prompt = f"""Current market trends:
{trend_summary}

Generate exactly 5 project ideas. Return only the JSON array."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        raw = response.content[0].text.strip()
        # Strip any accidental markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: return a safe default if parsing fails
            return [{
                "title": "LLM-Powered Security Log Analyzer",
                "description": "Use an LLM to interpret and triage security logs intelligently.",
                "stack": "Python, Anthropic API, AWS CloudWatch",
                "learning_goals": ["LLM tool use", "Security log analysis", "AWS integration"],
                "why_it_fits": "Directly combines your SIEM experience with AI"
            }]
