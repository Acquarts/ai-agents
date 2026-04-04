from datetime import datetime, timezone

from .news_fetcher import NewsFetcherAgent
from .summarizer import SummarizerAgent
from .storage_agent import StorageAgent, init_db


class OrchestratorAgent:
    def __init__(self):
        self.fetcher = NewsFetcherAgent()
        self.summarizer = SummarizerAgent()
        self.storage = StorageAgent()

    def run(self, top_n: int = 15) -> list[dict]:
        """Fetch, curate, and return today's top articles.

        Returns cached results if already run today.
        """
        init_db()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Check cache: did we already fetch today?
        cached = self.storage.get_articles_fetched_on(today)
        if cached:
            print(f"[orchestrator] Returning {len(cached)} cached articles for {today}")
            return cached

        # Fetch
        print("[orchestrator] Fetching articles...")
        raw_articles = self.fetcher.fetch_all()
        if not raw_articles:
            print("[orchestrator] No articles found")
            return []

        # Select & summarize in one Claude call
        print(f"[orchestrator] Selecting top {top_n} from {len(raw_articles)} articles...")
        curated = self.summarizer.select_and_summarize(raw_articles, top_n=top_n)
        print(f"[orchestrator] Got {len(curated)} curated articles")

        # Save to DB
        if curated:
            self.storage.save_articles(curated)
            run_id = self.storage.start_run()
            self.storage.finish_run(
                run_id,
                status="success",
                articles_fetched=len(raw_articles),
                articles_summarized=len(curated),
            )

        return curated
