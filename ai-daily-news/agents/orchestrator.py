from .storage_agent import StorageAgent, init_db
from .news_fetcher import NewsFetcherAgent
from .summarizer import SummarizerAgent


class OrchestratorAgent:
    def __init__(self):
        self.storage = StorageAgent()
        self.fetcher = NewsFetcherAgent()
        self.summarizer = SummarizerAgent()

    def run(self):
        print("[orchestrator] Initializing database...")
        init_db()

        print("[orchestrator] Starting pipeline run...")
        run_id = self.storage.start_run()

        try:
            # Step 1: Fetch news
            print("[orchestrator] Fetching articles...")
            raw_articles = self.fetcher.fetch_all()
            articles_fetched = len(raw_articles)
            print(f"[orchestrator] Fetched {articles_fetched} articles")

            # Step 2: Save raw articles
            saved = self.storage.save_articles(raw_articles)
            print(f"[orchestrator] Saved {saved} new articles to DB")

            # Step 3: Get unsummarized articles
            unsummarized = self.storage.get_unsummarized(limit=80)
            print(f"[orchestrator] {len(unsummarized)} articles need summarization")

            # Step 4: Summarize
            articles_summarized = 0
            if unsummarized:
                print("[orchestrator] Summarizing with Claude...")
                summarized = self.summarizer.summarize_batch(unsummarized)

                for art in summarized:
                    if art.get("summary"):
                        self.storage.update_summary(
                            art["id"],
                            art["summary"],
                            art["category"],
                            art["importance"],
                        )
                        articles_summarized += 1

                print(f"[orchestrator] Summarized {articles_summarized} articles")

            self.storage.finish_run(
                run_id,
                status="success",
                articles_fetched=articles_fetched,
                articles_summarized=articles_summarized,
            )
            print("[orchestrator] Pipeline completed successfully")

        except Exception as e:
            print(f"[orchestrator] Pipeline failed: {e}")
            self.storage.finish_run(run_id, status="error", error_message=str(e))
            raise
