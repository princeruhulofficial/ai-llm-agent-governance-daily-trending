#!/usr/bin/env python3
"""
AI · LLM · Agent Governance Daily Trending Tracker

Works with ANY OpenAI-compatible model (Grok, Claude via proxy, GPT, Gemini, local, OpenRouter...).
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pathlib import Path

import requests

# Add parent so we can import config
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")
LLM_API_KEY = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

if not GITHUB_TOKEN:
    print("❌ GITHUB_TOKEN is required")
    sys.exit(1)
if not LLM_API_KEY:
    print("❌ LLM_API_KEY (or OPENAI_API_KEY) is required")
    sys.exit(1)


# ---------------------------------------------------------------------------
# GitHub Search
# ---------------------------------------------------------------------------
def github_search(query: str, sort: str = "stars", page: int = 1) -> List[Dict]:
    """Search GitHub repositories. Returns list of repo items."""
    url = "https://api.github.com/search/repositories"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    params = {
        "q": query,
        "sort": sort,
        "order": "desc",
        "per_page": config.PER_PAGE,
        "page": page,
    }

    resp = requests.get(url, headers=headers, params=params, timeout=30)
    if resp.status_code == 403:
        print("⚠️  Rate limited by GitHub. Sleeping 60s...")
        time.sleep(60)
        resp = requests.get(url, headers=headers, params=params, timeout=30)

    if resp.status_code == 422:
        # Query too complex or invalid – skip silently
        return []

    resp.raise_for_status()
    data = resp.json()
    return data.get("items", [])


def collect_candidates() -> List[Dict[str, Any]]:
    """Run all category queries and return unique high-quality candidates."""
    date_filter = config.get_date_filter()
    seen = set()
    candidates = []

    print(f"🔍 Collecting candidates (lookback {config.RECENT_DAYS} days)...")

    for category, queries in config.CATEGORIES.items():
        print(f"\n📂 Category: {category}")
        for q in queries:
            full_q = f"{q} {date_filter} stars:>={config.MIN_STARS}"
            print(f"   → {full_q[:90]}...")

            try:
                # First by stars, then by updated for freshness
                for sort in ["stars", "updated"]:
                    items = github_search(full_q, sort=sort)
                    for item in items:
                        full_name = item["full_name"]
                        if full_name in seen:
                            continue
                        if item.get("stargazers_count", 0) < config.MIN_STARS:
                            continue
                        seen.add(full_name)
                        candidates.append({
                            "full_name": full_name,
                            "html_url": item["html_url"],
                            "description": (item.get("description") or "")[:300],
                            "stars": item.get("stargazers_count", 0),
                            "language": item.get("language") or "N/A",
                            "topics": item.get("topics", [])[:8],
                            "updated_at": item.get("updated_at", "")[:10],
                            "created_at": item.get("created_at", "")[:10],
                            "category_hint": category,
                        })
                    time.sleep(1.1)  # be nice to the API
            except Exception as e:
                print(f"   ⚠️  Query failed: {e}")
                continue

    # Sort by stars desc and truncate
    candidates.sort(key=lambda x: x["stars"], reverse=True)
    candidates = candidates[: config.MAX_CANDIDATES]

    print(f"\n✅ Collected {len(candidates)} unique candidates")
    return candidates


def format_candidates_for_prompt(candidates: List[Dict]) -> str:
    lines = []
    for i, c in enumerate(candidates, 1):
        topics = ", ".join(c["topics"]) if c["topics"] else "—"
        lines.append(
            f"{i}. **{c['full_name']}** ({c['stars']}★ · {c['language']} · updated {c['updated_at']})\n"
            f"   Category hint: {c['category_hint']}\n"
            f"   {c['description']}\n"
            f"   Topics: {topics}\n"
            f"   URL: {c['html_url']}"
        )
    return "\n\n".join(lines)


# ---------------------------------------------------------------------------
# LLM Call (any OpenAI-compatible endpoint)
# ---------------------------------------------------------------------------
def call_llm(system: str, user: str) -> str:
    url = f"{LLM_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.4,
        "max_tokens": 3500,
    }

    print(f"🧠 Calling LLM → {LLM_MODEL} @ {LLM_BASE_URL}")
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    if resp.status_code != 200:
        print(f"❌ LLM error {resp.status_code}: {resp.text[:500]}")
        resp.raise_for_status()

    data = resp.json()
    content = data["choices"][0]["message"]["content"]
    return content.strip()


# ---------------------------------------------------------------------------
# Create GitHub Issue
# ---------------------------------------------------------------------------
def create_issue(title: str, body: str) -> str:
    """Create a GitHub Issue in the current repository. Returns the issue URL."""
    # Detect owner/repo from the environment (set by GitHub Actions) or fall back
    repo_full = os.getenv("GITHUB_REPOSITORY")  # e.g. "princeruhulofficial/ai-llm-agent-governance-daily-trending"
    if not repo_full:
        # Local fallback – change if you want
        repo_full = "princeruhulofficial/ai-llm-agent-governance-daily-trending"

    owner, repo = repo_full.split("/")
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    payload = {
        "title": title,
        "body": body,
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code not in (200, 201):
        print(f"❌ Failed to create issue: {resp.status_code} {resp.text[:400]}")
        resp.raise_for_status()

    issue = resp.json()
    print(f"✅ Issue created: {issue['html_url']}")
    return issue["html_url"]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"🚀 Starting Daily Trending Tracker — {today}")
    print(f"   Model: {LLM_MODEL}")
    print(f"   Base URL: {LLM_BASE_URL}")

    candidates = collect_candidates()
    if not candidates:
        print("No candidates found. Exiting.")
        return

    candidates_text = format_candidates_for_prompt(candidates)

    system = config.SYSTEM_PROMPT.replace("{date}", today)
    user = config.USER_PROMPT_TEMPLATE.format(date=today, candidates=candidates_text)

    report = call_llm(system, user)

    # Safety: ensure the report starts reasonably
    if not report.startswith("#"):
        report = f"# 📅 Daily Trending Report — {today}\n\n" + report

    title = f"📅 Daily Trending: AI Agents · LLMs · Governance — {today}"

    # Add footer
    report += (
        f"\n\n---\n"
        f"*Generated on {today} using `{LLM_MODEL}` · "
        f"[Source code](https://github.com/{os.getenv('GITHUB_REPOSITORY', 'princeruhulofficial/ai-llm-agent-governance-daily-trending')})*\n"
    )

    issue_url = create_issue(title, report)
    print("\n🎉 Done!")
    print(f"   Issue: {issue_url}")


if __name__ == "__main__":
    main()
