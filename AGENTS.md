# Agent instructions

This repo holds personal agent skills, shipped as a Claude Code plugin and usable from Codex.

## Layout

- Each skill lives in `skills/<category>/<skill-name>/SKILL.md`.
- Categories are created only when the first skill needs one.
- Supporting files (references, templates, scripts) sit next to `SKILL.md` in the skill's folder.

## Writing a skill

- `SKILL.md` starts with frontmatter containing `name` (kebab-case, same as the folder) and `description`.
- The `description` says what the skill does and when to use it - it's what the agent reads to decide whether to load the skill.
- Keep `SKILL.md` short and focused on one job. Move long reference material into separate files and link to them.
- Write instructions for an agent, not for a human reader: concrete steps, no filler.

## Adding a skill

1. Create `skills/<category>/<skill-name>/SKILL.md`.
2. Add `"./skills/<category>/<skill-name>"` to the `skills` array in `.claude-plugin/plugin.json` (create the array if it doesn't exist yet).
3. Add the skill to the list in `README.md`.
4. Bump `version` in `.claude-plugin/plugin.json`.
