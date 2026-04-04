import sqlite3
import os
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "db" / "news.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS articles (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name     TEXT NOT NULL,
                source_url      TEXT NOT NULL,
                title           TEXT NOT NULL,
                original_url    TEXT NOT NULL UNIQUE,
                published_at    TEXT,
                fetched_at      TEXT NOT NULL,
                summary         TEXT,
                category        TEXT,
                importance      TEXT,
                raw_content     TEXT
            );

            CREATE TABLE IF NOT EXISTS runs (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at          TEXT NOT NULL,
                finished_at         TEXT,
                articles_fetched    INTEGER DEFAULT 0,
                articles_summarized INTEGER DEFAULT 0,
                status              TEXT,
                error_message       TEXT
            );
        """)


class StorageAgent:
    def save_articles(self, articles: list[dict]) -> int:
        if not articles:
            return 0
        saved = 0
        with get_connection() as conn:
            for art in articles:
                try:
                    conn.execute(
                        """
                        INSERT INTO articles
                            (source_name, source_url, title, original_url,
                             published_at, fetched_at, raw_content,
                             summary, category, importance)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(original_url) DO NOTHING
                        """,
                        (
                            art["source_name"],
                            art["source_url"],
                            art["title"],
                            art["original_url"],
                            art.get("published_at"),
                            art["fetched_at"],
                            art.get("raw_content", ""),
                            art.get("summary"),
                            art.get("category"),
                            art.get("importance"),
                        ),
                    )
                    if conn.execute("SELECT changes()").fetchone()[0] > 0:
                        saved += 1
                except Exception as e:
                    print(f"[storage] Error saving article '{art.get('title')}': {e}")
        return saved

    def update_summary(self, article_id: int, summary: str, category: str, importance: str):
        with get_connection() as conn:
            conn.execute(
                "UPDATE articles SET summary=?, category=?, importance=? WHERE id=?",
                (summary, category, importance, article_id),
            )

    def get_unsummarized(self, limit: int = 100) -> list[dict]:
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE summary IS NULL ORDER BY fetched_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_articles_fetched_on(self, date: str) -> list[dict]:
        """Get articles that were fetched on a given date (for cache check)."""
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM articles
                WHERE DATE(fetched_at) = ? AND summary IS NOT NULL
                ORDER BY
                    CASE importance WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                    published_at DESC
                """,
                (date,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_articles_for_date(self, date: str | None = None) -> list[dict]:
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT * FROM articles
                WHERE DATE(published_at) = ? AND summary IS NOT NULL
                ORDER BY
                    CASE importance WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                    published_at DESC
                """,
                (date,),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_latest_run(self) -> dict | None:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM runs ORDER BY id DESC LIMIT 1"
            ).fetchone()
        return dict(row) if row else None

    def start_run(self) -> int:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO runs (started_at, status) VALUES (?, 'running')",
                (datetime.now(timezone.utc).isoformat(),),
            )
            return cur.lastrowid

    def finish_run(
        self,
        run_id: int,
        status: str,
        articles_fetched: int = 0,
        articles_summarized: int = 0,
        error_message: str | None = None,
    ):
        with get_connection() as conn:
            conn.execute(
                """
                UPDATE runs
                SET finished_at=?, status=?, articles_fetched=?, articles_summarized=?, error_message=?
                WHERE id=?
                """,
                (
                    datetime.now(timezone.utc).isoformat(),
                    status,
                    articles_fetched,
                    articles_summarized,
                    error_message,
                    run_id,
                ),
            )
