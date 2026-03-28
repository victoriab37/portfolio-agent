"""
Evaluator agent — scores and ranks project ideas using Claude.
"""

import os
import json
import anthropic


class EvaluatorAgent:
    def __init__(self, profile: dict):
        self.profile = profile
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def rank(self, ideas: list) -> list:
        system_prompt = f"""You are a hiring manager at a top tech company evaluating portfolio projects.
Score each project idea for a candidate targeting: {', '.join(self.profile['target_roles'])}.

Scoring criteria (each out of 10, averaged):
- Resume impact: Does this impress a hiring manager in the target roles?
- Technical depth: Does it demonstrate real engineering skill?
- Learnability: Can it be built to a solid state in 1-3 weeks?
- Differentiation: Is it unique vs typical bootcamp projects?
- Skill leverage: Does it build on the candidate's existing strengths?

Respond ONLY with a valid JSON array of the same ideas, each with an added 'score' (float) and 'score_reasoning' (one sentence). Sort by score descending. No markdown, no preamble."""

        user_prompt = f"Score and rank these ideas:\n{json.dumps(ideas, indent=2)}"

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        raw = response.content[0].text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Return ideas with a default score if parsing fails
            for idea in ideas:
                idea["score"] = 7.0
                idea["score_reasoning"] = "Scored by default due to parsing error."
            return ideas
