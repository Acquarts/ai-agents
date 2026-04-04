import json
import os

import anthropic
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SYSTEM_PROMPT = """You are an AI news analyst. Your job is to read articles about artificial intelligence and produce concise, accurate summaries.

For each article you receive, output:
- summary: 2-3 sentences covering the key finding, announcement, or development. Be specific and informative.
- category: one of "Research" (papers, models, benchmarks), "Products" (launches, demos, apps), "Industry" (business, funding, policy), "Tooling" (libraries, frameworks, APIs, infrastructure)
- importance: "high" (major breakthrough or widely impactful), "medium" (notable development), "low" (minor or niche)

Always output valid JSON matching the provided schema. Never refuse an article — if content is minimal, do your best with what is available."""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
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
                "required": ["id", "summary", "category", "importance"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["results"],
    "additionalProperties": False,
}


def _chunks(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


class SummarizerAgent:
    def __init__(self):
        self.client = anthropic.Anthropic()

    def summarize_batch(self, articles: list[dict]) -> list[dict]:
        """Summarize a batch of articles. Returns articles with summary, category, importance filled in."""
        if not articles:
            return []

        results = []
        for batch in _chunks(articles, 5):
            batch_results = self._call_claude(batch)
            results.extend(batch_results)
        return results

    def _call_claude(self, batch: list[dict]) -> list[dict]:
        # Build user message with article content
        user_content = "Summarize these AI news articles:\n\n"
        for i, art in enumerate(batch):
            user_content += f"[{i}] Title: {art['title']}\n"
            user_content += f"Source: {art['source_name']}\n"
            if art.get("raw_content"):
                user_content += f"Content: {art['raw_content'][:800]}\n"
            user_content += "\n"

        try:
            response = self.client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=2048,
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
                        "description": "Submit the summaries for all articles in the batch",
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

            data = tool_use.input
            results_map = {r["id"]: r for r in data["results"]}

            enriched = []
            for i, art in enumerate(batch):
                result = results_map.get(i, {})
                enriched.append(
                    {
                        **art,
                        "summary": result.get("summary", ""),
                        "category": result.get("category", art.get("category_hint", "Industry")),
                        "importance": result.get("importance", "medium"),
                    }
                )
            return enriched

        except Exception as e:
            print(f"[summarizer] Claude API error: {e}")
            # Fallback: return articles with empty summaries
            return [
                {
                    **art,
                    "summary": "",
                    "category": art.get("category_hint", "Industry"),
                    "importance": "medium",
                }
                for art in batch
            ]
