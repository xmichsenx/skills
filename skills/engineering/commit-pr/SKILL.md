---
name: commit-pr
description: Conventions for git branches, commit messages, pull requests and squash merges. Use whenever creating a branch, writing a commit, opening a PR or merging one.
---

# Commits, branches and PRs

All branch names, commit messages and PR text are in English, even when the conversation is in another language.

## Branches

- Format: `<type>/<short-kebab-case-description>`, e.g. `feat/add-edge-tts`, `fix/empty-payload-crash`.
- `<type>` is one of the commit types below.
- Never commit directly to the default branch; create a branch first.

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <description>

<optional body>
```

- Types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `style`, `build`, `ci`, `chore`.
- Description: imperative mood, lowercase start, no trailing period, under ~72 characters. `feat: add edge TTS voice selection`, not `Added voices.`
- Scope: only when the repo has clear modules and the scope adds information, e.g. `fix(api): handle empty payload`. Otherwise omit it.
- Body: add one for non-obvious changes. Leave a blank line after the title and explain *why*, not *what* - the diff shows what.
- Keep commits small and atomic: one logical change per commit. Split unrelated changes (e.g. a refactor and a feature) into separate commits. Each commit should leave the project working.

## Pull requests

- Title: the branch name, e.g. `feat/add-edge-tts`.
- Description: a short, general summary of what changed. A few sentences or bullets, no template sections.
- Before opening, make sure the branch is pushed and checks pass locally where the repo has them.

## Merging

- Use squash merge.
- Rewrite the squash commit title as a Conventional Commit with the PR number, not the branch name: `feat: add edge TTS (#3)`, not `feat/add-edge-tts (#3)`.
- With the GitHub CLI: `gh pr merge <number> --squash --subject "feat: add edge TTS (#3)" --delete-branch`.
