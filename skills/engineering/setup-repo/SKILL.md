---
name: setup-repo
description: Interactively set up a GitHub repository with the gh CLI - create the repo and remote, add missing repo files, CI checks, main branch protection, labels, issue/PR templates, Dependabot and security settings. Audits the current state first and asks the user before changing anything. Use when the user wants to create, bootstrap, configure or harden a GitHub repo.
---

# Set up a GitHub repository

Interview-driven setup. You audit, propose, ask, then apply - never change anything on GitHub or in the repo without the user's confirmation.

## Rules

- **Ask with recommendations.** Use the harness's question tool if one exists (e.g. `AskUserQuestion`), otherwise ask in chat. Batch related questions per area. Put the recommended option first and mark it `(Recommended)`.
- **Only ask what you can't detect.** Read the repo and GitHub state first; don't ask about things that are already configured unless the user wants to change them.
- **Idempotent.** Running the skill twice must not duplicate labels, rulesets or workflows. Update existing items instead of creating new ones.
- **Confirm before applying.** After the questions, show one summary of every change (files to add, API calls to make) and wait for a clear yes.
- **Verify after applying** and report what actually happened, including anything that failed.

## 1. Preflight

- `gh auth status` - must be logged in. Pushing workflow files needs the `workflow` scope; if missing, ask the user to run `gh auth refresh -s workflow`.
- Find the repo: `git remote get-url origin` and `gh repo view --json nameWithOwner,visibility,defaultBranchRef`. No remote or no git repo is fine - that's area A.

## 2. Audit

Collect the current state and show it to the user as a short checklist (configured / missing) per area:

| Area | How to check |
| --- | --- |
| A. Repo + remote | git repo, commits, `origin`, GitHub repo exists |
| B. Repo files | `.gitignore`, `LICENSE`, `README.md` |
| C. CI checks | `.github/workflows/*.yml`, stack and existing scripts |
| D. Protection + merge | `gh api repos/{owner}/{repo}/rulesets`, merge settings |
| E. Labels | `gh label list --limit 200` |
| F. Issue/PR templates | `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` |
| G. Dependabot + security | `.github/dependabot.yml`, `gh api repos/{owner}/{repo} --jq .security_and_analysis`, `gh api repos/{owner}/{repo}/vulnerability-alerts` (204 = on, 404 = off) |

Then ask which areas to set up (multi-select). Recommend all missing ones.

## 3. Interview and apply, area by area

For each chosen area, read its reference file, ask its questions, and collect the planned changes:

- A, B → [references/repo.md](references/repo.md)
- C → [references/ci.md](references/ci.md)
- D → [references/protection.md](references/protection.md)
- E → [references/labels.md](references/labels.md)
- F → [references/templates.md](references/templates.md)
- G → [references/security.md](references/security.md)

Show the full summary, get confirmation, then apply in this order:

1. **A** - create the repo and remote.
2. **B, C, F, G files** - commit them. Follow the `commit-pr` skill for commit messages and branches if it's available.
   - New repo without protection: commit straight to the default branch and push.
   - Repo already protected: put them on a branch and open a PR. Wait for checks before merging, and ask before merging.
3. **G settings, E** - API calls.
4. **D last** - so CI has run at least once (required check names exist) and setup commits weren't blocked.

## 4. Verify and report

- Re-run the audit and show the before/after checklist.
- Protection: `gh api repos/{owner}/{repo}/rules/branches/{default_branch}` lists the active rules.
- CI: link the latest workflow run (`gh run list --limit 1`).
- List anything skipped or failed, with the error and what the user can do about it.
