# 🤖 AI Agents

A hands-on repository exploring the world of AI agents, from simple single-agent setups to complex multi-agent orchestrations.

## What Are AI Agents?

AI agents are autonomous systems that can perceive their environment, make decisions, and take actions to achieve specific goals. Unlike traditional chatbots that simply respond to prompts, agents can:

- **Reason** about complex problems step by step
- **Use tools** to interact with external systems (search, APIs, databases)
- **Collaborate** with other agents to tackle multi-step tasks
- **Remember** context across interactions
- **Adapt** their behavior based on feedback

## What You'll Find Here

This repository is a collection of practical examples, experiments, and ready-to-run implementations covering:

### 🧠 Agent Architectures
- Single-agent systems with tool usage
- Multi-agent orchestration and delegation
- Sequential, parallel, and loop workflows
- Hierarchical agent structures

### 🔧 Tools & Integrations
- Web search and information retrieval
- RAG (Retrieval-Augmented Generation) pipelines
- API integrations and function calling
- Vector databases for semantic search

### 🛠️ Frameworks & SDKs
- Google ADK (Agent Development Kit)
- LangChain and LangGraph
- OpenAI Agents SDK
- Custom implementations

### 🚀 Deployment Patterns
- Local development and testing
- API endpoints with FastAPI
- Containerized agents with Docker
- Cloud deployment strategies

## Tech Stack

```
Orchestration:   Google ADK, LangChain, LangGraph
LLMs:            Gemini, GPT, Claude
Vector DBs:      Pinecone, ChromaDB, FAISS
APIs:            FastAPI, Flask
Deployment:      Docker, AWS, Streamlit
Automation:      n8n, custom pipelines
```

## Getting Started

Each project includes its own setup instructions, but the general flow is:

```bash
# Clone the repository
git clone https://github.com/Acquarts/ai-agents.git
cd ai-agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Configure your API keys
cp .env.example .env
# Edit .env with your keys (GOOGLE_API_KEY, OPENAI_API_KEY, etc.)
```

## Why This Repository?

Building AI agents is the next frontier in applied AI. This repo exists to:

- 📚 **Learn by doing** — real code, real examples, no fluff
- 🔬 **Experiment freely** — test different architectures and approaches
- 🏗️ **Build production-ready systems** — patterns that scale
- 🤝 **Share knowledge** — everything I learn goes here

## Resources

If you're new to AI agents, here are some helpful starting points:

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI Function Calling Guide](https://platform.openai.com/docs/guides/function-calling)
- [Building Effective Agents (Anthropic)](https://www.anthropic.com/research/building-effective-agents)

## Connect

- 🌐 Portfolio: [azafuture.com](https://www.azafuture.com)
- 💼 LinkedIn: [adrianzambranaacquaroni](https://linkedin.com/in/adrianzambranaacquaroni)
- 🐙 GitHub: [Acquarts](https://github.com/Acquarts)

---

*Building agents that actually work.* 🚀
