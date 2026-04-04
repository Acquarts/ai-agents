import html
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone

import feedparser
import requests

from .sources import RSS_SOURCES

FETCH_TIMEOUT = 15  # seconds per source
MAX_AGE_HOURS = 48  # skip articles older than this


def _strip_html(text: str) -> str:
    if not text:
        return ""
    text = html.unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:2000]  # cap raw content length


def _parse_time(entry) -> str | None:
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        try:
            dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            return dt.isoformat()
        except Exception:
            pass
    return None


def _fetch_source(source: dict) -> list[dict]:
    name = source["name"]
    url = source["url"]
    try:
        response = requests.get(url, timeout=FETCH_TIMEOUT, headers={"User-Agent": "AINewsAgent/1.0"})
        response.raise_for_status()
        feed = feedparser.parse(response.content)
    except Exception as e:
        print(f"[fetcher] Failed to fetch {name}: {e}")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=MAX_AGE_HOURS)
    articles = []

    for entry in feed.entries:
        link = getattr(entry, "link", None)
        title = getattr(entry, "title", None)
        if not link or not title:
            continue

        published_at = _parse_time(entry)
        if published_at:
            try:
                pub_dt = datetime.fromisoformat(published_at)
                if pub_dt < cutoff:
                    continue
            except Exception:
                pass

        content = ""
        if hasattr(entry, "content") and entry.content:
            content = _strip_html(entry.content[0].get("value", ""))
        elif hasattr(entry, "summary"):
            content = _strip_html(entry.summary)
        elif hasattr(entry, "description"):
            content = _strip_html(entry.description)

        articles.append(
            {
                "source_name": name,
                "source_url": url,
                "title": _strip_html(title),
                "original_url": link,
                "published_at": published_at,
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "raw_content": content,
                "category_hint": source.get("category_hint", "Industry"),
            }
        )

    print(f"[fetcher] {name}: {len(articles)} articles")
    return articles


class NewsFetcherAgent:
    def fetch_all(self) -> list[dict]:
        all_articles: list[dict] = []
        seen_urls: set[str] = set()

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(_fetch_source, src): src for src in RSS_SOURCES}
            for future in as_completed(futures):
                for art in future.result():
                    if art["original_url"] not in seen_urls:
                        seen_urls.add(art["original_url"])
                        all_articles.append(art)

        print(f"[fetcher] Total unique articles: {len(all_articles)}")
        return all_articles
