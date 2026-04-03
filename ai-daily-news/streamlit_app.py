import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

import streamlit as st

DB_PATH = Path(__file__).parent / "db" / "news.db"

CATEGORY_COLORS = {
    "Research": "blue",
    "Products": "violet",
    "Industry": "green",
    "Tooling": "orange",
}

IMPORTANCE_LABELS = {
    "high": ":red[**★ High**]",
    "medium": ":orange[**Medium**]",
    "low": "Low",
}


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_articles(date: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM articles
            WHERE fetched_at LIKE ? AND summary IS NOT NULL
            ORDER BY
                CASE importance WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END,
                published_at DESC
            """,
            (f"{date}%",),
        ).fetchall()
    return [dict(r) for r in rows]


def get_latest_run() -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM runs ORDER BY id DESC LIMIT 1"
        ).fetchone()
    return dict(row) if row else None


def format_date_es(iso: str | None) -> str:
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%d %b, %H:%M")
    except Exception:
        return ""


# --- Page config ---
st.set_page_config(page_title="AI News Daily", page_icon="🤖", layout="wide")

# --- Ensure DB exists ---
if not DB_PATH.exists():
    DB_PATH.parent.mkdir(exist_ok=True)
    with sqlite3.connect(str(DB_PATH)) as conn:
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

# --- Header ---
st.title("🤖 AI News Daily")

# --- Date selector ---
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
dates = {}
for offset in range(0, 7):
    d = datetime.now(timezone.utc) - timedelta(days=offset)
    d_str = d.strftime("%Y-%m-%d")
    if offset == 0:
        label = "Hoy"
    elif offset == 1:
        label = "Ayer"
    else:
        label = d.strftime("%a %d")
    dates[label] = d_str

cols = st.columns(len(dates))
if "selected_date" not in st.session_state:
    st.session_state.selected_date = today

for col, (label, d_str) in zip(cols, dates.items()):
    with col:
        if st.button(
            label,
            key=f"date_{d_str}",
            use_container_width=True,
            type="primary" if st.session_state.selected_date == d_str else "secondary",
        ):
            st.session_state.selected_date = d_str
            st.rerun()

selected_date = st.session_state.selected_date

# --- Run info ---
run_info = get_latest_run()
if run_info:
    status_icon = "🟢" if run_info["status"] == "success" else "🔴"
    finished = run_info.get("finished_at", "")
    finished_str = format_date_es(finished) if finished else "en progreso"
    st.caption(
        f"{status_icon} Última actualización: {finished_str} · "
        f"{run_info.get('articles_fetched', 0)} recuperados · "
        f"{run_info.get('articles_summarized', 0)} resumidos"
    )

# --- Load articles ---
articles = get_articles(selected_date)

if not articles:
    st.divider()
    st.markdown(
        f"### 📰 Sin noticias para {selected_date}\n\n"
        "El pipeline se ejecuta diariamente. Para ejecutarlo manualmente:\n\n"
        "```\npython agents/run_pipeline.py\n```"
    )
    st.stop()

# --- Stats ---
high_count = sum(1 for a in articles if a.get("importance") == "high")
col1, col2, col3 = st.columns(3)
col1.metric("Noticias", len(articles))
if high_count:
    col2.metric("Alta importancia", high_count)

# --- Category counts ---
categories = {}
for a in articles:
    cat = a.get("category", "Industry")
    categories[cat] = categories.get(cat, 0) + 1

# --- Category filter ---
st.divider()
filter_options = ["Todas"] + list(categories.keys())
active_filter = st.radio(
    "Categoría",
    filter_options,
    horizontal=True,
    format_func=lambda x: f"{x} ({categories[x]})" if x in categories else x,
    label_visibility="collapsed",
)

filtered = (
    articles
    if active_filter == "Todas"
    else [a for a in articles if a.get("category") == active_filter]
)

# --- Articles grid ---
cols_per_row = 3
for i in range(0, len(filtered), cols_per_row):
    row = filtered[i : i + cols_per_row]
    cols = st.columns(cols_per_row)
    for col, article in zip(cols, row):
        with col:
            importance = article.get("importance", "medium")
            category = article.get("category", "Industry")
            cat_color = CATEGORY_COLORS.get(category, "gray")

            with st.container(border=True):
                # Tags row
                imp_label = IMPORTANCE_LABELS.get(importance, importance)
                st.markdown(f"{imp_label} &nbsp; :{cat_color}[{category}]")

                # Title
                st.markdown(f"**[{article['title']}]({article['original_url']})**")

                # Summary
                if article.get("summary"):
                    st.caption(article["summary"])

                # Footer
                pub_date = format_date_es(article.get("published_at") or article.get("fetched_at"))
                st.markdown(
                    f"<small style='color:gray'>{article['source_name']} · {pub_date}</small>",
                    unsafe_allow_html=True,
                )
