# News Agent — Automated Tech News Aggregator & Notification System

A fully automated **AI-powered news agent** that fetches trending tech news from 20+ RSS sources, summarizes articles using local or cloud LLMs, ranks them by relevance, and delivers a curated digest straight to your **Telegram** (and optionally WhatsApp).

> Built with **LangGraph** — a stateful, graph-based pipeline orchestrator.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Pipeline Flow](#pipeline-flow)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Supported RSS Sources](#supported-rss-sources)
- [Memory & Trends](#memory--trends)
- [Roadmap](#roadmap)

---

## How It Works

The agent runs as a **sequence of LangGraph nodes**, each responsible for one stage of the news pipeline:

```
RSS Feeds → Fetch → Deduplicate → Filter (memory) → Rank → Summarize → Critic → Notify → Update Memory
                                              ↑                                ↑
                                          (history.json)                  (trends.json)
```

1. **Fetch** — Pulls articles from 20+ tech RSS feeds (TechCrunch, HN, Reddit, Hugging Face, OpenAI, etc.)
2. **Filter** — Deduplicates by title, then removes articles already seen (loaded from `data/memory/history.json`)
3. **Rank** — Scores articles using keyword matching + source authority weights + trending-word boosts
4. **Summarize** — Condenses each article into a 1‑line (≤50 word) summary via Ollama (local) or HuggingFace API
5. **Critic** — Removes summaries shorter than 10 characters (noise filter)
6. **Notify** — Formats the digest and sends it via Telegram
7. **Memory** — Logs seen articles into `history.json` and updates trending-word frequencies in `trends.json`

---

## Pipeline Flow


The graph is compiled with LangGraph's `StateGraph`:

| Step | Node | Service | What It Does |
|------|------|---------|-------------|
| 1 | `fetch` | `rss_service.fetch_articles()` | Parses RSS feeds → `Article` objects |
| 2 | `filter` | `cleaner.deduplicate()` + `memory_service.filter_new_articles()` | Removes duplicates & already‑seen articles |
| 3 | `rank` | `ranking_service.rank_articles()` | Scores by keywords + source weight + trend boost |
| 4 | `summarize` | `llm_service.summarize()` | LLM‑powered 1‑line summarization |
| 5 | `critic` | inline filter | Drops very short summaries |
| 6 | `notify` | `notification_service.send_all()` | Sends formatted digest to Telegram |
| 7 | `memory` | `memory_service.update_memory()` + `update_trends()` | Persists seen titles & trending words |

---

## Architecture

```
news_agent/
├── agents/               # LangGraph graph definition
│   ├── graph.py          # StateGraph builder & compile
│   ├── nodes.py          # 7 pipeline nodes (fetch → memory)
│   └── state.py          # NewsState TypedDict
├── core/
│   └── config.py         # RSS feeds, API keys, model settings from .env
├── models/
│   └── article.py        # Article dataclass (title, summary, source)
├── services/
│   ├── rss_service.py        # Feedparser-based RSS ingestion
│   ├── memory_service.py     # JSON-backed history & trend tracking
│   ├── ranking_service.py    # Keyword + source + trend scoring
│   ├── llm_service.py        # Ollama / HuggingFace summarization
│   ├── notification_service.py # Telegram (plus commented-out WhatsApp)
│   └── news_pipeline.py      # (legacy) non-graph pipeline
├── utils/
│   ├── cleaner.py        # Title-based deduplication
│   ├── formatter.py      # Digest message formatting
│   └── logger.py         # File-based logging to logs/news_agent.log
└── main.py               # Entry point — builds & runs the graph
```

### State

The `NewsState` TypedDict flows through the graph:

```python
class NewsState(TypedDict):
    articles: list            # Raw articles from RSS
    filtered_articles: list   # After dedup + memory filter
    ranked_articles: list     # After scoring
    summaries: list           # After LLM summarization + critic
```

---

## Features

- **Graph‑Based Orchestration** — Uses LangGraph for explicit, observable state transitions
- **20+ RSS Sources** — Covers major tech news, AI labs, developer communities, and Reddit
- **Smart Ranking** — Keyword scoring (AI, startup, Nvidia, etc.) + source authority weights + trending‑word boost
- **Dual LLM Support** — Ollama (local, default `qwen2.5:1.5b`) or HuggingFace API with 3‑model fallback chain
- **Persistent Memory** — `history.json` prevents re‑delivering read articles; `trends.json` detects emerging topics
- **Telegram Notifications** — Instant delivery via bot API
- **Logging** — Structured logs at `logs/news_agent.log`
- **Battery‑Included** — Single `run_agent.bat` to activate venv + launch

---

## Project Structure

```
agent/
├── README.md
├── requirements.txt          # Dependencies
├── run_agent.bat             # Windows launch script
├── .env                      # (your) API keys & tokens
├── data/
│   ├── memory/
│   │   ├── history.json      # Seen article titles (last 200)
│   │   └── trends.json       # Word frequency counter
│   ├── processed.py          # (legacy)
│   └── processed/
├── logs/
│   └── news_agent.log        # Runtime logs
├── news_agent/               # Main package
│   ├── main.py
│   ├── agents/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   └── state.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   │   └── article.py
│   ├── services/
│   │   ├── rss_service.py
│   │   ├── memory_service.py
│   │   ├── ranking_service.py
│   │   ├── llm_service.py
│   │   ├── notification_service.py
│   │   ├── news_pipeline.py
│   │   └── storage_service.py
│   └── utils/
│       ├── cleaner.py
│       ├── formatter.py
│       └── logger.py
├── tests/
│   ├── test_model.py
│   └── test_watsapp.py
└── graphify-out/              # Knowledge graph artifacts (graphify)
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- (Optional) [Ollama](https://ollama.com/) for local LLM inference
- Telegram bot token (from [@BotFather](https://t.me/BotFather))

### 1. Clone & Virtual Environment

```bash
git clone https://github.com/kaustubhreet/news_agent.git
cd news_agent

# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
# --- LLM Provider ---
MODEL_PROVIDER=ollama          # "ollama" or "hf"
OLLAMA_URL=http://localhost:11434/api/generate   # (ollama only)
MODEL_NAME=qwen2.5:1.5b                           # (ollama only)
HF_API_KEY=hf_your_token_here                     # (hf only)

# --- Notifications ---
TELEGRAM_TOKEN=your_bot_token_from_botfather
CHAT_ID=your_telegram_chat_id
PHONE_NO=+91XXXXXXXXXX        # (optional, for WhatsApp — currently commented out)
```

If using **Ollama**, pull the model:

```bash
ollama pull qwen2.5:1.5b
```

---

## Usage

### Run the Agent

```bash
# Windows
run_agent.bat

# Or manually:
python -m news_agent.main
```

The agent will:
1. Fetch ~500 articles from 20+ feeds
2. Filter to new + unique articles
3. Rank and pick the top 25
4. Summarize each via LLM
5. Send the digest to your Telegram

### Logging

All activity is logged to `logs/news_agent.log` with timestamps and severity levels.

---

## Supported RSS Sources

| Category | Sources |
|----------|---------|
| **Tech News** | TechCrunch, ArsTechnica, Wired, Engadget, The Verge |
| **Cybersecurity** | The Hacker News |
| **Aggregators** | Hacker News, hnRSS (AI‑filtered), Product Hunt |
| **Reddit** | r/LocalLLaMA, r/MachineLearning, r/ArtificialIntelligence, r/technology |
| **AI Labs** | Hugging Face Blog, OpenAI, Google DeepMind, AWS ML Blog |
| **AI Engineering** | Unite.ai, InfoQ AI/ML/Data Engineering |

Configured in `news_agent/core/config.py` — easy to add/remove feeds.

---

## Memory & Trends

### `data/memory/history.json`

Stores the last **200 seen article titles**. Used in the `filter` node to skip articles already delivered — prevents duplicate notifications across runs.

### `data/memory/trends.json`

A running word‑frequency counter built from article titles + summaries each run. The top frequent words (excluding stopwords) are fed back into the ranking node via `boost_with_trends()` to surface trending topics higher in the digest.

---

## Ranking Algorithm (`ranking_service.py`)

Articles are scored via three signals:

1. **Keyword Match** (+2 per hit) — Keywords: AI, OpenAI, Google, Microsoft, Nvidia, Anthropic, LLM, GPT, startup, funding, India, chip, acquisition, layoff, engineer, agent, huggingface
2. **Source Authority** (+2 to +5) — TechCrunch=5, The Verge=4, Wired=3, hnRSS/HN=2, FeedBurner=3
3. **Trend Boost** (+3 per trending word) — Words that appeared frequently across the current batch get an extra score bump

---

## Tests

```bash
python -m pytest tests/
```

Current tests:
- `test_model.py` — Article dataclass validation
- `test_watsapp.py` — WhatsApp functionality (legacy)

---

## Roadmap

- [ ] WhatsApp notification (via `pywhatkit` / web automation)
- [ ] Email digest option
- [ ] Web dashboard for browsing past digests
- [ ] Per‑user topic preferences & filtering
- [ ] Scheduled execution (cron / Task Scheduler)
- [ ] Multi‑language summarization
- [ ] Vector‑based semantic deduplication

---

## License

MIT

---

## Acknowledgments

- [LangGraph](https://langchain-ai.github.io/langgraph/) for the graph orchestration framework
- [Feedparser](https://feedparser.readthedocs.io/) for RSS parsing
- [Ollama](https://ollama.com/) for local LLM inference
- All the RSS sources that make this possible