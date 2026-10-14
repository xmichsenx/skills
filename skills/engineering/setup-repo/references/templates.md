# F. Issue and PR templates

Keep them minimal - short templates get filled in, long ones get deleted.

## Questions

- **Which templates** (multi-select) - PR template, bug report, feature request. Recommend all three.
- **Blank issues** - allow them (recommended for personal repos) or force the forms.

## Apply

`.github/pull_request_template.md` - a short description of what changed, matching the `commit-pr` convention:

```markdown
## What changed

<!-- A short, general summary of the change. -->
```

`.github/ISSUE_TEMPLATE/bug.yml`:

```yaml
name: Bug report
description: Something doesn't work as expected
labels: [fix]
body:
  - type: textarea
    id: what
    attributes:
      label: What happened
      description: What you expected, what happened instead, and how to reproduce it.
    validations:
      required: true
```

`.github/ISSUE_TEMPLATE/feature.yml`:

```yaml
name: Feature request
description: Suggest a new feature or improvement
labels: [feat]
body:
  - type: textarea
    id: what
    attributes:
      label: What and why
      description: What should be added or changed, and why it's useful.
    validations:
      required: true
```

`.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: true
```

The `labels` in the forms must exist (area E); if the user skipped labels, drop the `labels` lines.
