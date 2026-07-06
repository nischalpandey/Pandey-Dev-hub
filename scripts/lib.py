"""Shared helpers for the Resource Hub automation scripts."""
import json
import os
import re
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(REPO_ROOT, "data", "repositories.json")
RULES_FILE = os.path.join(REPO_ROOT, "data", "category_rules.json")

GITHUB_URL_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)/?(?:\.git)?/?$"
)


def parse_github_url(url: str):
    """Return (owner, repo) tuple or None if the URL isn't a valid repo URL."""
    if not url:
        return None
    url = url.strip()
    match = GITHUB_URL_RE.match(url)
    if not match:
        return None
    return match.group("owner"), match.group("repo")


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return default
        return json.loads(content)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def load_repositories():
    return load_json(DATA_FILE, [])


def save_repositories(repos):
    save_json(DATA_FILE, repos)


def load_category_rules():
    return load_json(RULES_FILE, {"order": [], "rules": {}, "fallback": "Other Resources"})


def github_api_get(path: str):
    """Call the GitHub REST API and return parsed JSON. Uses GITHUB_TOKEN if present."""
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    url = f"https://api.github.com{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "resource-hub-bot",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"GitHub API error {e.code} for {url}: {body}") from e


def fetch_repo_metadata(owner: str, repo: str) -> dict:
    """Fetch the fields we need to render the README for a single repo."""
    data = github_api_get(f"/repos/{owner}/{repo}")

    topics = data.get("topics") or []
    license_info = data.get("license") or {}

    return {
        "full_name": data.get("full_name", f"{owner}/{repo}"),
        "html_url": data.get("html_url", f"https://github.com/{owner}/{repo}"),
        "description": (data.get("description") or "No description provided.").strip(),
        "stars": data.get("stargazers_count", 0),
        "forks": data.get("forks_count", 0),
        "language": data.get("language") or "N/A",
        "topics": topics,
        "license": license_info.get("spdx_id") or "N/A",
        "updated_at": (data.get("pushed_at") or data.get("updated_at") or "")[:10],
        "archived": bool(data.get("archived", False)),
    }


def categorize(metadata: dict, explicit_category: str = None) -> str:
    """Pick a category: explicit choice wins, else match keywords, else fallback."""
    rules_cfg = load_category_rules()
    order = rules_cfg.get("order", [])
    rules = rules_cfg.get("rules", {})
    fallback = rules_cfg.get("fallback", "Other Resources")

    if explicit_category and explicit_category.strip() and explicit_category.strip().lower() != "auto-detect":
        return explicit_category.strip()

    haystack = " ".join(
        [metadata.get("language") or ""] + (metadata.get("topics") or [])
    ).lower()

    for category in order:
        keywords = rules.get(category, [])
        for kw in keywords:
            if kw.lower() in haystack:
                return category

    return fallback


def normalize_url(url: str) -> str:
    parsed = parse_github_url(url)
    if not parsed:
        return url.strip().rstrip("/")
    owner, repo = parsed
    return f"https://github.com/{owner}/{repo}"


def eprint(*args):
    print(*args, file=sys.stderr)
