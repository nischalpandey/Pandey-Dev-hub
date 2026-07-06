"""
Add a single GitHub repository URL to data/repositories.json.

Usage:
    python scripts/add_repo.py "<repo_url>" ["<category>"]

Reads REPO_URL / CATEGORY env vars as a fallback so it can be driven
directly from a GitHub Actions workflow input.
"""
import os
import sys

from lib import (
    load_repositories,
    save_repositories,
    normalize_url,
    parse_github_url,
    eprint,
)

TODAY_FMT = "%Y-%m-%d"


def main():
    import datetime

    repo_url = None
    category = None

    if len(sys.argv) > 1:
        repo_url = sys.argv[1]
    if len(sys.argv) > 2:
        category = sys.argv[2]

    repo_url = repo_url or os.environ.get("REPO_URL")
    category = category or os.environ.get("CATEGORY")

    if not repo_url:
        eprint("ERROR: no repository URL provided.")
        sys.exit(1)

    parsed = parse_github_url(repo_url)
    if not parsed:
        eprint(f"ERROR: '{repo_url}' does not look like a valid https://github.com/<owner>/<repo> URL.")
        sys.exit(1)

    clean_url = normalize_url(repo_url)
    repos = load_repositories()

    existing_urls = {r["url"] for r in repos}
    if clean_url in existing_urls:
        print(f"Repository already in the collection, skipping: {clean_url}")
        return

    entry = {
        "url": clean_url,
        "category": category.strip() if category and category.strip().lower() != "auto-detect" else None,
        "added_date": datetime.date.today().strftime(TODAY_FMT),
    }
    repos.append(entry)
    save_repositories(repos)
    print(f"Added: {clean_url} (category hint: {entry['category'] or 'auto-detect'})")


if __name__ == "__main__":
    main()
