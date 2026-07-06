# Setup Guide

## 1. Create the GitHub repository
Create a new **public** repository (e.g. `pandey-dev-hub`) and push everything
in this folder to it (including the `.github` folder — it's easy to miss since it's hidden).

```bash
cd pandey-dev-hub
git init
git add .
git commit -m "Initial commit: resource hub scaffold"
git branch -M main
git remote add origin https://github.com/<you>/<your-repo>.git
git push -u origin main
```

## 2. Enable Actions
Go to the repo's **Settings → Actions → General → Workflow permissions** and select
**"Read and write permissions"**. This lets the bot commit README updates and close
issues using the built-in `GITHUB_TOKEN` (no extra secrets or personal access token needed).

## 3. Update placeholder links
In `.github/ISSUE_TEMPLATE/config.yml`, replace `YOUR_USERNAME/YOUR_REPO` with your
actual repo path. This is cosmetic (only affects the issue-template chooser link) —
everything else works without it.

## 4. Add your first repository
Pick whichever you like best:

- **Issue form (recommended)**: go to *Issues → New Issue → ➕ Add Repository*,
  paste a URL like `https://github.com/aishwaryanr/awesome-generative-ai-guide`,
  optionally pick a category, submit. A bot will add it, rebuild the README, comment,
  and close the issue — usually within ~30 seconds.
- **Manual workflow**: go to *Actions → Add Repository (Manual) → Run workflow*,
  paste the URL (and optional category), run it.

## 5. That's it
From here on:
- New repos → paste a URL via an issue or the manual workflow.
- Stats (stars/forks/description) refresh automatically every night via the
  **Refresh README Metadata** workflow (`.github/workflows/refresh-readme.yml`),
  and you can also trigger it manually from the Actions tab any time.
- Categories are inferred from GitHub topics/language using
  `data/category_rules.json` — edit that file's keyword lists any time to
  reclassify future additions (existing entries can be recategorized by editing
  their `category` field in `data/repositories.json` and re-running the refresh
  workflow).

## Notes
- No personal access token or secret is required — the workflows use the
  automatically-provided `GITHUB_TOKEN`, which gives a 1,000 requests/hour
  budget against the GitHub API, plenty for this use case.
- Adding a repo that's already in the collection is a safe no-op (deduped by URL).
- If a submitted URL is invalid or a repo can't be fetched (private, deleted,
  renamed), it's skipped with a warning in the workflow log rather than
  breaking the README.
