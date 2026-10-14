# C. CI checks

Build CI from tools the project **already has**. Don't introduce a new linter, formatter or test runner without asking.

## Detect

| Stack | Signals | Check commands |
| --- | --- | --- |
| Node/TS | `package.json`; lockfile picks the package manager (`package-lock.json` → npm, `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock(b)` → bun) | scripts named `lint`, `typecheck`/`type-check`, `test`, `build` |
| Python | `pyproject.toml`, `requirements*.txt`; `uv.lock` → uv | tools configured in `pyproject.toml` or present in deps: `ruff`, `mypy`/`pyright`, `pytest` |
| Other | `go.mod`, `Cargo.toml`, ... | the stack's standard build/test commands |

Also check existing `.github/workflows/` - extend or fix those rather than adding duplicates.

## Questions

- **Which checks** (multi-select) - list only the commands that exist; recommend all of them.
- **Missing tools** - if there's no linter or tests at all, say so and ask whether to add one. Recommend skipping for now unless the user wants it; never add one silently.
- **Triggers** - recommend `push` to the default branch and all `pull_request`s.
- **Runtime version** - read it from the project (`.nvmrc`, `engines`, `.python-version`, `requires-python`). Ask only if nothing pins it.

## Apply

- One workflow file, `.github/workflows/ci.yml`, one job per check or one job with several steps. Prefer separate jobs only when checks are slow; otherwise one job named `ci` keeps the required-checks list short.
- **Job names are the required-check names** used in area D. Keep them short and stable (`ci`, `lint`, `test`), and tell the user that renaming a job breaks the required check.
- Use the current major versions of `actions/checkout`, `actions/setup-node`, `actions/setup-python`, `astral-sh/setup-uv` - check their releases rather than relying on memory.
- Enable dependency caching through the setup action (`cache: npm`, `enable-cache: true` for uv, etc.).
- Install with the lockfile (`npm ci`, `pnpm install --frozen-lockfile`, `uv sync --locked`).
- Before committing, run the same commands locally if possible, so the first CI run doesn't fail on something you could have caught.

Minimal shape:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      # setup + install + checks for the detected stack
```
