# D. Branch protection + merge settings

Use a **repository ruleset** (not legacy branch protection). On the Free plan rulesets only apply to public repos - if the API returns 403 on a private repo, tell the user and stop this area.

## Questions

Recommended defaults first:

- **Require a pull request** - yes, 0 required approvals (a solo owner can't approve their own PR). Alternative: no PR requirement.
- **Required status checks** - yes, every CI job from area C (or existing workflows). Skip the rule if the repo has no CI.
- **Extra rules** (multi-select) - block force pushes (recommended), block deletion (recommended), require linear history (recommended).
- **Bypass for repo admins** - "pull requests only" (recommended): admins can merge a PR past the rules, but can't push directly. Alternatives: always, never.
- **Merge methods** - squash only (recommended). Alternatives: squash + rebase, all.
- **Delete head branches after merge** - yes (recommended).

## Apply

Check for an existing ruleset targeting the default branch first (`gh api repos/{owner}/{repo}/rulesets`). If one exists, update it with `PUT .../rulesets/{id}` instead of creating a second one.

Write the ruleset to a temp file and create it:

```bash
gh api -X POST repos/{owner}/{repo}/rulesets --input ruleset.json
```

Full recommended ruleset - drop the rules the user declined:

```json
{
  "name": "main protection",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [
    { "actor_id": 5, "actor_type": "RepositoryRole", "bypass_mode": "pull_request" }
  ],
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    { "type": "required_linear_history" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": false,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": false
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": false,
        "required_status_checks": [{ "context": "ci", "integration_id": 15368 }]
      }
    }
  ]
}
```

- `actor_id: 5` is the built-in **Repository admin** role. `bypass_mode`: `"pull_request"` (PRs only) or `"always"`; for "never", use `"bypass_actors": []`.
- `context` is the CI **job name**; `integration_id: 15368` is GitHub Actions. Add one entry per required job.
- `required_linear_history` needs merge commits disabled, otherwise the merge button offers an option the rule rejects.

Merge settings (adjust to the user's answers):

```bash
gh api -X PATCH repos/{owner}/{repo} -F allow_squash_merge=true -F allow_merge_commit=false -F allow_rebase_merge=false -F delete_branch_on_merge=true
```

## Verify

- `gh api repos/{owner}/{repo}/rules/branches/main` lists the active rules.
- Optionally (ask first): try `git push` of an empty commit straight to `main`, expect "push declined due to repository rule violations", then `git reset --hard origin/main` to drop the test commit.
