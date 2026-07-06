<div align="center">

# 🚀 Pandey DevHub

### A curated, auto-updating directory of great GitHub repositories — no forks, just links.

![Repositories](https://img.shields.io/badge/Repositories-0-blue?style=flat-square) ![Categories](https://img.shields.io/badge/Categories-0-informational?style=flat-square) ![Last%20Updated](https://img.shields.io/badge/Last%20Updated-2026--07--06-success?style=flat-square) ![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen?style=flat-square) ![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)

**No forks. No clutter. Just a clean, always-current map of great repos.**

[➕ Add a repository](../../issues/new?template=add-repository.yml) · [📖 How it works](#-how-it-works)

</div>

---


## 📭 No repositories yet

This hub is empty — be the first to add one! Open an [**Add Repository**](../../issues/new?template=add-repository.yml) issue and paste a GitHub URL, or trigger the *Add Repository (Manual)* workflow from the Actions tab.

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
<sub>Last generated on 2026-07-06 • Powered by GitHub Actions</sub>
</div>
