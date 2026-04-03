# AI Daily News

Pipeline automatizado de noticias de inteligencia artificial. Recopila articulos de multiples fuentes RSS, los resume con Claude (Haiku) y los presenta en un dashboard Streamlit.

## Arquitectura

```
agents/
  sources.py          # Fuentes RSS (HuggingFace, ArXiv, OpenAI, Google AI, etc.)
  news_fetcher.py     # Fetch concurrente de feeds RSS
  summarizer.py       # Resumenes con Claude API (Haiku 4.5)
  storage_agent.py    # Persistencia en SQLite
  orchestrator.py     # Orquesta el pipeline completo
  run_pipeline.py     # Entry point del pipeline

scheduler/
  register_task.py    # Tarea programada (Windows Task Scheduler)

streamlit_app.py      # Dashboard web
db/news.db            # Base de datos SQLite (se crea automaticamente)
```

## Requisitos

- Python 3.12+
- API key de Anthropic

## Instalacion

```bash
pip install -r requirements.txt
```

Crear un archivo `.env` en la raiz del proyecto:

```
ANTHROPIC_API_KEY=sk-ant-...
```

## Uso

### Ejecutar el pipeline

```bash
python agents/run_pipeline.py
```

Esto hace:
1. Fetch de articulos de 9 fuentes RSS (HuggingFace, ArXiv, MIT Tech Review, VentureBeat, The Verge, OpenAI, Google AI, DeepMind, Towards Data Science)
2. Guarda articulos nuevos en SQLite
3. Resume con Claude Haiku los articulos sin resumen
4. Clasifica por categoria (Research, Products, Industry, Tooling) e importancia (high, medium, low)

### Ver el dashboard

```bash
streamlit run streamlit_app.py
```

### Programar ejecucion diaria (Windows)

```bash
python scheduler/register_task.py
```

Registra una tarea en Windows Task Scheduler que ejecuta el pipeline todos los dias a las 7:00 AM.

## Deploy en Streamlit Cloud

1. Subir el repositorio a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repo y seleccionar `streamlit_app.py`
4. Configurar el secret `ANTHROPIC_API_KEY` en la configuracion de la app

> **Nota:** Streamlit Cloud usa almacenamiento efimero. Para produccion, considera usar una base de datos externa (PostgreSQL, Supabase, etc.) en lugar de SQLite.

## Stack

- **Claude Haiku 4.5** — resumenes y clasificacion de articulos
- **Streamlit** — dashboard web
- **SQLite** — almacenamiento local
- **feedparser** — parsing de RSS
- **Anthropic SDK** — cliente de la API de Claude
