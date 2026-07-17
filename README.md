# 🤖 AI · LLM · Agent Governance Daily Trending Tracker

**Anyone can run this.**  
Daily curated list of the most interesting **trending GitHub repositories** in:

- 🤖 **AI Agents** & Agentic systems (LangGraph, CrewAI, AutoGen, multi-agent, tool-calling, MCP, etc.)
- 🧠 **LLMs** (open models, inference, RAG, fine-tuning, evaluation, benchmarks)
- 🛡️ **AI Governance / Safety / Ethics / Alignment** (policy, red-teaming, constitutional AI, responsible AI, audit, least-privilege, etc.)

Built for people who care about **making AI accountable** — especially those building or using agentic systems.

---

## ✨ Why this exists

GitHub Trending is noisy.  
This tracker uses smart search + any LLM you choose to surface only the high-signal repos that matter for **agents + governance**.

Perfect for:
- Founders & engineers working on AI agents
- Safety / governance researchers
- Teams who want daily signal without doomscrolling

---

## 🚀 How it works (for everyone)

1. GitHub Actions runs every day (or you run the script manually)
2. Uses GitHub Search API to find recent high-quality candidates in the 3 categories
3. Sends the candidate list to **any LLM** you want (Grok, Claude, GPT-4o, Gemini, local models via OpenAI-compatible endpoint…)
4. The LLM curates the best ones and writes a clean Markdown report
5. Creates a dated **GitHub Issue** with the full report

All reports live forever in the Issues tab.

---

## 🛠️ Setup for yourself (5 minutes)

### 1. Fork this repository

### 2. Add Secrets (Settings → Secrets and variables → Actions)

| Secret Name       | Required | Description |
|-------------------|----------|-------------|
| `GITHUB_TOKEN`    | Yes (auto) | Already provided by GitHub Actions. Needs `issues: write` + `contents: read` |
| `LLM_API_KEY`     | Yes      | Your API key (xAI / OpenAI / Anthropic / OpenRouter / Together / Fireworks / local…) |
| `LLM_BASE_URL`    | Optional | Default: `https://api.openai.com/v1`<br>For Grok: `https://api.x.ai/v1`<br>For OpenRouter: `https://openrouter.ai/api/v1` etc. |
| `LLM_MODEL`       | Optional | Default: `gpt-4o-mini`<br>Examples: `grok-4`, `claude-3-5-sonnet-20241022`, `gpt-4o`, `gemini-2.0-flash` |

### 3. Enable Actions

Go to **Actions** tab → enable workflows if asked.

### 4. (Optional) Customize

Edit `config.py` to change search queries, number of results, categories, or the system prompt.

---

## 🖥️ Run locally (any model, any time)

```bash
git clone https://github.com/YOUR_USERNAME/ai-llm-agent-governance-daily-trending.git
cd ai-llm-agent-governance-daily-trending

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Set environment variables
export GITHUB_TOKEN=ghp_xxxxxxxx
export LLM_API_KEY=your_key_here
export LLM_BASE_URL=https://api.x.ai/v1      # optional
export LLM_MODEL=grok-4                      # optional

python src/tracker.py
```

This will:
- Search repositories
- Call your LLM
- Create a new Issue in **your** forked repo

---

## 📁 Project Structure

```
.
├── .github/workflows/daily.yml   # Daily cron + manual trigger
├── src/
│   └── tracker.py                # Main logic (search + LLM + create issue)
├── config.py                     # Easy to edit: queries, categories, prompt
├── requirements.txt
└── README.md
```

---

## 🎯 Categories & Search Strategy

We intentionally use multiple targeted GitHub Search queries (topics + keywords + recency + stars) so we catch both established frameworks and brand-new high-velocity projects.

The LLM then acts as a smart curator focused on **relevance to agent reliability, safety, and governance**.

---

## 🤝 Contributing

- Improve the search queries in `config.py`
- Make the prompt better
- Add more categories (e.g. MCP servers, agent frameworks, evaluation)
- Add Discord / Telegram / email notification options
- PRs welcome!

---

## 🇧🇩 Built with ❤️ from Bangladesh

Created by [@princeruhulofficial](https://github.com/princeruhulofficial) — Founder of **Prevalid** (Making AI Accountable).

If this helps you stay on top of the agentic + governance wave, please ⭐ the repo and share it.

---

**Powered by any model you choose + GitHub Actions**  
No vendor lock-in. Fully open.
