"""
Regenerate README.md from data/repositories.json using live GitHub metadata.

Usage:
    python scripts/generate_readme.py
"""
import datetime
import os
import sys

from lib import (
    REPO_ROOT,
    load_repositories,
    load_category_rules,
    fetch_repo_metadata,
    parse_github_url,
    categorize,
    eprint,
)

README_PATH = os.path.join(REPO_ROOT, "README.md")

HUB_TITLE = os.environ.get("HUB_TITLE", "Pandey DevHub")
HUB_TAGLINE = os.environ.get(
    "HUB_TAGLINE",
    "A curated, auto-updating directory of great GitHub repositories — no forks, just links.",
)

ANCHOR_EMOJI = {
    "AI & Machine Learning": "🤖",
    "Data Science": "📊",
    "Web Development": "🌐",
    "Mobile Development": "📱",
    "DevOps & Infrastructure": "🛠️",
    "Security": "🔐",
    "Game Development": "🎮",
    "Developer Tools": "🧰",
    "Other Resources": "📦",
}


def slugify(text: str) -> str:
    return text.lower().replace(" & ", "--").replace(" ", "-").replace("'", "")


def badge(label: str, value: str, color: str) -> str:
    label_enc = label.replace(" ", "%20")
    value_enc = str(value).replace(" ", "%20").replace("-", "--")
    return f"![{label}](https://img.shields.io/badge/{label_enc}-{value_enc}-{color}?style=flat-square)"


def star_badge(url: str) -> str:
    return f"![Stars](https://img.shields.io/github/stars/{url}?style=flat-square&label=%E2%AD%90)"


def build_table(entries: list) -> str:
    lines = [
        "| Repository | Description | ⭐ Stars | 🍴 Forks | Language | Updated |",
        "|---|---|---|---|---|---|",
    ]
    for e in entries:
        name = e["full_name"]
        link = e["html_url"]
        desc = e["description"].replace("|", "\\|")
        if len(desc) > 110:
            desc = desc[:107].rstrip() + "..."
        lines.append(
            f"| [**{name}**]({link}) | {desc} | {e['stars']:,} | {e['forks']:,} | {e['language']} | {e['updated_at']} |"
        )
    return "\n".join(lines)


def main():
    repos = load_repositories()
    rules_cfg = load_category_rules()
    order = rules_cfg.get("order", [])

    if not repos:
        write_readme({}, order, total=0, failures=[])
        print("No repositories yet — wrote placeholder README.")
        return

    categorized = {}
    failures = []

    for entry in repos:
        parsed = parse_github_url(entry["url"])
        if not parsed:
            failures.append((entry["url"], "invalid URL"))
            continue
        owner, repo = parsed
        try:
            meta = fetch_repo_metadata(owner, repo)
        except Exception as exc:  # noqa: BLE001
            eprint(f"WARNING: failed to fetch {owner}/{repo}: {exc}")
            failures.append((entry["url"], str(exc)))
            continue

        category = categorize(meta, entry.get("category"))
        categorized.setdefault(category, []).append(meta)

    for cat in categorized:
        categorized[cat].sort(key=lambda m: m["stars"], reverse=True)

    total = sum(len(v) for v in categorized.values())
    write_readme(categorized, order, total, failures)
    print(f"README.md regenerated with {total} repositories across {len(categorized)} categories.")
    if failures:
        print(f"{len(failures)} repositories could not be fetched — see warnings above.")


def write_readme(categorized: dict, order: list, total: int, failures: list):
    today = datetime.date.today().isoformat()

    ordered_categories = [c for c in order if c in categorized]
    ordered_categories += [c for c in categorized if c not in order]

    header = f"""<div align="center">

# 🚀 {HUB_TITLE}

### {HUB_TAGLINE}

{badge("Repositories", total, "blue")} {badge("Categories", len(categorized), "informational")} {badge("Last%20Updated", today, "success")} {badge("PRs", "Welcome", "brightgreen")} {badge("License", "MIT", "lightgrey")}

**No forks. No clutter. Just a clean, always-current map of great repos.**

[➕ Add a repository](../../issues/new?template=add-repository.yml) · [📖 How it works](#-how-it-works)

</div>

---
"""

    if total == 0:
        body = (
            "\n## 📭 No repositories yet\n\n"
            "This hub is empty — be the first to add one! "
            "Open an [**Add Repository**](../../issues/new?template=add-repository.yml) issue "
            "and paste a GitHub URL, or trigger the *Add Repository (Manual)* workflow from the Actions tab.\n"
        )
        toc = ""
    else:
        toc_lines = ["## 📚 Categories\n"]
        for cat in ordered_categories:
            count = len(categorized[cat])
            emoji = ANCHOR_EMOJI.get(cat, "📁")
            toc_lines.append(f"- {emoji} [{cat}](#{slugify(cat)}) `{count}`")
        toc = "\n".join(toc_lines) + "\n"

        section_lines = []
        for cat in ordered_categories:
            emoji = ANCHOR_EMOJI.get(cat, "📁")
            entries = categorized[cat]
            section_lines.append(f"\n## {emoji} {cat}\n")
            section_lines.append(build_table(entries))
            section_lines.append("")
        body = "\n".join(section_lines)

    footer = f"""
---

## ✨ How it works

This hub never forks anything — it just tracks links plus live metadata pulled from the GitHub API.

1. **Add a repository**
   - Easiest: open an [**Add Repository** issue](../../issues/new?template=add-repository.yml), paste the GitHub URL, optionally pick a category, submit.
   - Or: run the **Add Repository (Manual)** workflow from the *Actions* tab and fill in the inputs.
2. A GitHub Actions workflow validates the URL, appends it to [`data/repositories.json`](data/repositories.json), and fetches live stats (stars, forks, language, description, last updated).
3. If no category is given, the repository is **auto-categorized** from its GitHub topics/language using the rules in [`data/category_rules.json`](data/category_rules.json).
4. `README.md` is fully regenerated and committed automatically. No manual editing, ever.

Metadata is refreshed automatically on a schedule too, so stars/forks/descriptions stay current even for repos added long ago.

## 🤝 Contributing

Found a great repo that's missing? Open an [Add Repository issue](../../issues/new?template=add-repository.yml) — that's it.

---

<div align="center">
<sub>Last generated on {today} • Powered by GitHub Actions</sub>
</div>
"""

    content = header + "\n" + toc + body + footer

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    main()
