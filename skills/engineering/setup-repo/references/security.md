# G. Dependabot and security

## Questions

- **Security settings** (multi-select, all recommended):
  - Dependabot alerts - notify about vulnerable dependencies.
  - Dependabot security updates - automatic PRs fixing those vulnerabilities.
  - Secret scanning + push protection - block pushes containing tokens/keys. Free for public repos; private repos need GitHub Advanced Security, so skip there unless the API accepts it.
- **Dependabot version updates** - regular PRs bumping dependencies. Recommend yes, weekly, grouped into one PR per ecosystem so it doesn't flood the repo. Alternatives: monthly, security updates only.

## Apply settings

```bash
gh api -X PUT repos/{owner}/{repo}/vulnerability-alerts
gh api -X PUT repos/{owner}/{repo}/automated-security-fixes
```

Secret scanning and push protection - write the payload to a temp file:

```json
{
  "security_and_analysis": {
    "secret_scanning": { "status": "enabled" },
    "secret_scanning_push_protection": { "status": "enabled" }
  }
}
```

```bash
gh api -X PATCH repos/{owner}/{repo} --input security.json
```

Check the result with `gh api repos/{owner}/{repo} --jq .security_and_analysis`. Report any setting that stayed disabled instead of retrying.

## Apply version updates

`.github/dependabot.yml` - one entry per detected ecosystem, plus `github-actions` whenever there are workflows. Ecosystem names: `npm` (also pnpm/yarn), `uv`, `pip`, `gomod`, `cargo`, `docker`, `github-actions`.

```yaml
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
    groups:
      dependencies:
        patterns: ["*"]
    commit-message:
      prefix: chore
      include: scope
    labels: [chore]

  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
    groups:
      actions:
        patterns: ["*"]
    commit-message:
      prefix: ci
    labels: [ci]
```

`commit-message.prefix` keeps Dependabot PRs in Conventional Commit style (`chore(deps): ...`, `ci: ...`). The labels must exist (area E); if the user skipped labels, drop the `labels` lines.
