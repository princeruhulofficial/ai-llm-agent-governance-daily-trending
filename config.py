"""
Easy-to-edit configuration for the Daily Trending Tracker.
Change search queries, categories, or the LLM prompt here.
"""

from datetime import datetime, timedelta, timezone

# How many candidates to pull per search query (max 100, but keep low for rate limits)
PER_PAGE = 12

# How many total unique candidates to send to the LLM
MAX_CANDIDATES = 35

# Minimum stars to consider (helps filter noise)
MIN_STARS = 8

# Look back window for "recent" activity (days)
RECENT_DAYS = 60

# Categories and their GitHub search queries
# Simplified to avoid GitHub Search 422 errors (complex OR + date filters)
CATEGORIES = {
    "AI Agents": [
        'topic:ai-agents',
        'topic:agentic-ai',
        'topic:multi-agent-systems',
        'topic:langgraph',
        'topic:crewai',
        'topic:autogen',
        '"ai agent" stars:>20',
        '"agent framework" OR "tool calling"',
        'topic:mcp OR "model context protocol"',
    ],
    "LLMs": [
        'topic:llm',
        'topic:large-language-models',
        'topic:rag',
        'topic:retrieval-augmented-generation',
        '"open weight" OR "open-weight" model',
        'vllm OR "llama.cpp" OR sglang',
        'topic:llm-evaluation OR "llm benchmark"',
    ],
    "AI Governance & Safety": [
        'topic:ai-safety',
        'topic:ai-alignment',
        'topic:ai-governance',
        'topic:responsible-ai',
        '"ai governance" OR "agent governance"',
        '"ai safety" OR red-teaming',
        '"prompt injection" OR topic:prompt-injection',
        '"audit trail" OR "data provenance" AI',
    ],
}


def get_date_filter() -> str:
    """Return the GitHub search date filter for recent repos."""
    since = (datetime.now(timezone.utc) - timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%d")
    return f"pushed:>{since}"


# System prompt for the LLM curator
SYSTEM_PROMPT = """You are an expert curator specializing in AI Agents, Large Language Models, and AI Governance/Safety/Ethics.

Your job is to select the most important, high-signal, and currently relevant GitHub repositories from a candidate list and write a clean daily report.

Prioritize:
1. Repositories that advance **agent reliability, safety, observability, or governance**
2. New or rapidly rising projects (even if fewer stars) that solve real pain points
3. High-quality frameworks, tools, evaluation suites, or research code
4. Things that Prevalid-style "AI Execution OS" or accountability layers would care about

Avoid:
- Pure marketing / demo repos with no real code
- Extremely generic "awesome lists" unless they are exceptional
- Repos that are already ancient and not actively evolving

Output format (strict Markdown):

# 📅 Daily Trending Report — {date}

> Curated by AI · Focus: Agents + LLMs + Governance

## 🔥 Top Picks

### 1. [owner/repo](url)
- **Stars**: X · **Language**: Y · **Category**: Agents / LLM / Governance
- **Why it matters**: One sharp sentence.
- **Key insight**: Optional second sentence if valuable.

### 2. ...

(Continue for 8–12 best repos. Group loosely by category if it helps readability.)

## 📌 Quick Notes
- 1–3 bullet points of overall trends you noticed today.

End with:
---
*Report generated automatically. Star the repo if useful!*
"""


# User prompt template
USER_PROMPT_TEMPLATE = """Today's date: {date}

Here is a list of candidate repositories gathered from GitHub Search (sorted by relevance + stars + recency):

{candidates}

Please select the best 8–12 and write the daily report following the exact format in the system instructions.
Focus especially on anything useful for people building safe, accountable, and production-ready AI agents.
"""
