# E. Labels

Labels mirror the Conventional Commit types, plus a few statuses.

## Recommended set

| Name | Color | Description |
| --- | --- | --- |
| `feat` | `0E8A16` | New feature |
| `fix` | `D73A4A` | Bug fix |
| `refactor` | `C5DEF5` | Code change without behavior change |
| `perf` | `FBCA04` | Performance improvement |
| `test` | `BFD4F2` | Tests |
| `docs` | `0075CA` | Documentation |
| `ci` | `5319E7` | CI and workflows |
| `chore` | `EDEDED` | Maintenance, tooling, dependencies |
| `blocked` | `B60205` | Blocked by something else |
| `needs-info` | `D876E3` | Waiting for more information |

## Questions

- **Label set** - the recommended set above (recommended), or let the user add/remove labels.
- **GitHub's default labels** (`accessibility`, `bug`, `enhancement`, `documentation`, `duplicate`, `good first issue`, `help wanted`, `invalid`, `question`, `wontfix`) - recommend deleting them, since the set above replaces them. Only offer to delete labels that aren't used: check with `gh issue list --label <name> --state all --limit 1` and `gh pr list --label <name> --state all --limit 1`. Never delete a used label without asking about it by name.

## Apply

- Create or update (idempotent):

  ```bash
  gh label create <name> --color <hex> --description "<desc>" --force
  ```

- Delete: `gh label delete <name> --yes`.
- If Dependabot is configured (area G), make sure the labels it uses exist (`chore`, `ci`).
