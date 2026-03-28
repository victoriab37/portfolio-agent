"""
Research agent — uses Tavily to search for current trends.
"""

import os
import requests


class ResearchAgent:
    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.base_url = "https://api.tavily.com/search"

    def search(self, query: str) -> str:
        if not self.api_key:
            return f"[Tavily not configured — set TAVILY_API_KEY to enable live research]"

        try:
            response = requests.post(
                self.base_url,
                json={
                    "api_key": self.api_key,
                    "query": query,
                    "search_depth": "basic",
                    "max_results": 3,
                },
                timeout=10,
            )
            data = response.json()
            results = data.get("results", [])
            snippets = [r.get("content", "")[:200] for r in results]
            return " | ".join(snippets)
        except Exception as e:
            return f"[Search failed: {e}]"
