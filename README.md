# GitHub Trending AI Agents ·
**Daily curated trending repositories** focused on:

- **AI Agents** & Agentic systems (LangGraph, CrewAI, AutoGen, multi-agent, tool-calling, MCP)
- **LLMs** (open models, inference, RAG, fine-tuning, evaluation)
- **AI Governance / Safety / Alignment** (policy, red-teaming, responsible AI, audit)

> Built for people who care about **making AI accountable**.

[![Daily Run](https://github.com/princeruhulofficial/github-trending/actions/workflows/daily.yml/badge.svg)](https://github.com/princeruhulofficial/github-trending/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Stars](https://img.shields.io/github/stars/princeruhulofficial/github-trending?style=social)](https://github.com/princeruhulofficial/github-trending)

---

## Why this exists

GitHub Trending is noisy.  
This tracker uses smart GitHub Search + **any LLM you choose** to surface only the high-signal repos that matter for **agents + governance**.

Perfect for:
- Founders & engineers building AI agents
- Safety / governance researchers
- Teams who want daily signal without doomscrolling

---

## How it works

1. GitHub Actions runs every day (or manual trigger)
2. Uses GitHub Search API to find recent high-quality candidates
3. Sends candidates to **any OpenAI-compatible LLM** (Grok, Claude, GPT, OpenRouter free models, local models…)
4. LLM curates the best ones and writes a clean Markdown report
5. Creates a dated **GitHub Issue** with the full report

All reports live forever in the **Issues** tab.

---

## Quick Setup (5 minutes)

### 1. Fork this repository

### 2. Add Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Required | Example |
|--------|----------|---------|
| `LLM_API_KEY` | Yes | Your OpenRouter / xAI / OpenAI key |
| `LLM_BASE_URL` | Optional | `https://openrouter.ai/api/v1` |
| `LLM_MODEL` | Optional | `openrouter/free` or `grok-4` |

### 3. Enable Actions

Go to the **Actions** tab and enable workflows.

### 4. Run it

- Wait for the daily cron, **or**
- Click **Run workflow** manually

---

## Run Locally

```bash
git clone https://github.com/princeruhulofficial/github-trending.git
cd github-trending

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export GITHUB_TOKEN=ghp_xxxxxxxx
export LLM_API_KEY=your_key_here
export LLM_BASE_URL=https://openrouter.ai/api/v1
export LLM_MODEL=openrouter/free

python src/tracker.py
```

---

## Project Structure

```
.
├── .github/workflows/daily.yml   # Daily cron + manual trigger
├── src/tracker.py                # Main logic
├── config.py                     # Easy to edit queries & prompt
├── requirements.txt
└── README.md
```

---

## Keywords this repo targets

`github trending` · `ai agents trending` · `llm trending` · `agentic ai` · `ai governance` · `ai safety` · `mcp servers` · `multi agent systems` · `daily trending github` · `open source ai tools`

---

## Built with ❤️ from Bangladesh

Created by [Prince Ruhul](https://github.com/princeruhulofficial) — Founder of **[Prevalid](https://www.prevalid.net)** (Making AI Accountable).

If this helps you stay on top of the agentic + governance wave, please **⭐ the repo** and share it.

---

**Powered by any model you choose + GitHub Actions**  
No vendor lock-in. Fully open source.
