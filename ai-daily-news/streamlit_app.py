import sys
import os
from datetime import datetime, timezone

import streamlit as st

# Ensure agents package is importable
sys.path.insert(0, os.path.dirname(__file__))
from agents.orchestrator import OrchestratorAgent

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
st.title("🤖 AI News Daily")

# --- Fetch articles (cached for the session / day) ---
@st.cache_data(ttl=3600, show_spinner=False)
def get_today_news():
    agent = OrchestratorAgent()
    return agent.run(top_n=15)


with st.spinner("Buscando las noticias más relevantes de hoy..."):
    articles = get_today_news()

if not articles:
    st.info("No se encontraron noticias de IA hoy. Inténtalo más tarde.")
    st.stop()

# --- Stats ---
now = datetime.now(timezone.utc)
st.caption(f"🟢 {len(articles)} noticias curadas · {now.strftime('%d %b %Y, %H:%M')} UTC")

high_count = sum(1 for a in articles if a.get("importance") == "high")
col1, col2 = st.columns(2)
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
                imp_label = IMPORTANCE_LABELS.get(importance, importance)
                st.markdown(f"{imp_label} &nbsp; :{cat_color}[{category}]")
                st.markdown(f"**[{article['title']}]({article['original_url']})**")
                if article.get("summary"):
                    st.caption(article["summary"])
                pub_date = format_date_es(
                    article.get("published_at") or article.get("fetched_at")
                )
                st.markdown(
                    f"<small style='color:gray'>{article['source_name']} · {pub_date}</small>",
                    unsafe_allow_html=True,
                )

# --- Refresh button ---
st.divider()
if st.button("🔄 Actualizar noticias", use_container_width=True):
    st.cache_data.clear()
    st.rerun()
