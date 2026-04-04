import os

import anthropic
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SYSTEM_PROMPT = """You are an AI news curator. You receive a list of recent AI articles and must:

1. Select the 15 most relevant and impactful articles
2. Summarize each in 2-3 sentences
3. Classify each by category and importance

Prioritize: major breakthroughs, product launches, significant funding/policy news, and widely useful tools.
Skip: minor updates, duplicates covering the same story (pick the best one), and overly niche content.

Always output valid JSON matching the provided schema."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {
                        "type": "integer",
                        "description": "Original article index from the input list",
                    },
                    "summary": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": ["Research", "Products", "Industry", "Tooling"],
                    },
                    "importance": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                    },
                },
                "required": ["index", "summary", "category", "importance"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


class SummarizerAgent:
    def __init__(self):
        self.client = anthropic.Anthropic()

    def select_and_summarize(self, articles: list[dict], top_n: int = 15) -> list[dict]:
        """Select the top_n most relevant articles and summarize them in one call."""
        if not articles:
            return []

        user_content = f"Select the {top_n} most relevant AI news articles and summarize them:\n\n"
        for i, art in enumerate(articles):
            user_content += f"[{i}] {art['title']}"
            if art.get("source_name"):
                user_content += f" ({art['source_name']})"
            if art.get("raw_content"):
                user_content += f"\n    {art['raw_content'][:300]}"
            user_content += "\n\n"

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=4096,
                timeout=60.0,
                system=[
                    {
                        "type": "text",
                        "text": SYSTEM_PROMPT,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[{"role": "user", "content": user_content}],
                tools=[
                    {
                        "name": "submit_summaries",
                        "description": "Submit the curated and summarized articles",
                        "input_schema": OUTPUT_SCHEMA,
                    }
                ],
                tool_choice={"type": "tool", "name": "submit_summaries"},
            )

            tool_use = next(
                (b for b in response.content if b.type == "tool_use"), None
            )
            if not tool_use:
                raise ValueError("No tool_use block in response")

            selected = []
            for r in tool_use.input["results"]:
                idx = r["index"]
                if 0 <= idx < len(articles):
                    selected.append(
                        {
                            **articles[idx],
                            "summary": r["summary"],
                            "category": r["category"],
                            "importance": r["importance"],
                        }
                    )
            return selected

        except Exception as e:
            print(f"[summarizer] Claude API error: {e}")
            return []
