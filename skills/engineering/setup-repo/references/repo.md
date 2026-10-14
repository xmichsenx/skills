# A. Repo + remote, B. Repo files

## A. Questions

Skip any that the audit already answers.

- **Name** - recommend the local folder name.
- **Owner** - the user's account (`gh api user --jq .login`) or one of their orgs (`gh org list`).
- **Visibility** - public or private. Mention that branch rulesets on private repos need a paid plan (GitHub Pro/Team); on the Free plan protection (area D) only works on public repos.
- **Description** - one line, optional.

## A. Apply

- No git repo: `git init -b main`.
- No commits yet: create the files from B first, then make the initial commit (`chore: initial commit`).
- Create and connect in one step:

  ```bash
  gh repo create <owner>/<name> --public|--private --description "<desc>" --source . --remote origin --push
  ```

- Repo exists on GitHub but no local remote: `git remote add origin https://github.com/<owner>/<name>.git`, then `git push -u origin main`.
- Remote exists but GitHub repo doesn't: create it without `--source` (`gh repo create <owner>/<name> --public|--private`), then push.

## B. Questions

Only for missing files.

- **`.gitignore`** - detect the stack (`package.json` → Node, `pyproject.toml`/`requirements.txt` → Python, etc.). Recommend GitHub's template for it; list available ones with `gh api gitignore/templates`. Merge with any existing entries the user needs (e.g. `.env`, `.claude/settings.local.json`).
- **`LICENSE`** - recommend MIT for public repos, none for private ones. Ask the copyright holder name; don't guess it from the git config.
- **`README.md`** - recommend a short skeleton: title, one-line description, how to install/run, license.

## B. Apply

- `.gitignore`: `gh api gitignore/templates/<Name> --jq .source > .gitignore`.
- `LICENSE`: `gh api licenses/<key> --jq .body`, then replace `[year]` and `[fullname]`.
- `README.md`: write the skeleton with real commands from the project (scripts in `package.json`, `pyproject.toml`), not placeholders.
