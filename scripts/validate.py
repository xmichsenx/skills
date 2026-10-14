"""Validate plugin manifests and skills. Stdlib only.

Usage: python scripts/validate.py
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_DIR = ROOT / ".claude-plugin"
SKILLS_DIR = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        error(f"{path.relative_to(ROOT).as_posix()}: file not found")
    except json.JSONDecodeError as e:
        error(f"{path.relative_to(ROOT).as_posix()}: invalid JSON ({e})")
    return None


def parse_frontmatter(path: Path) -> dict[str, str] | None:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep and not line.startswith((" ", "\t")):
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def check_manifests() -> list[str]:
    marketplace = load_json(PLUGIN_DIR / "marketplace.json")
    plugin = load_json(PLUGIN_DIR / "plugin.json")
    if plugin is None:
        return []

    for field in ("name", "version", "description"):
        if not plugin.get(field):
            error(f"plugin.json: missing '{field}'")

    plugin_names = [p.get("name") for p in marketplace.get("plugins", [])] if marketplace else []
    if marketplace and plugin.get("name") not in plugin_names:
        error(f"marketplace.json: no plugin entry named '{plugin.get('name')}'")

    skills = plugin.get("skills", [])
    if not isinstance(skills, list):
        error("plugin.json: 'skills' must be a list")
        return []
    return skills


def check_skills(listed: list[str]) -> None:
    listed_dirs = set()
    for entry in listed:
        skill_dir = (ROOT / entry).resolve()
        listed_dirs.add(skill_dir)
        if not (skill_dir / "SKILL.md").is_file():
            error(f"plugin.json: '{entry}' has no SKILL.md")

    found_dirs = {p.parent.resolve() for p in SKILLS_DIR.rglob("SKILL.md")} if SKILLS_DIR.exists() else set()
    for skill_dir in sorted(found_dirs - listed_dirs):
        error(f"{skill_dir.relative_to(ROOT).as_posix()}: not listed in plugin.json 'skills'")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for skill_dir in sorted(found_dirs):
        rel = skill_dir.relative_to(ROOT).as_posix()
        fm = parse_frontmatter(skill_dir / "SKILL.md")
        if fm is None:
            error(f"{rel}/SKILL.md: missing frontmatter")
            continue
        name = fm.get("name", "")
        if not name:
            error(f"{rel}/SKILL.md: missing 'name'")
        elif name != skill_dir.name:
            error(f"{rel}/SKILL.md: name '{name}' doesn't match folder '{skill_dir.name}'")
        elif not NAME_RE.match(name):
            error(f"{rel}/SKILL.md: name '{name}' must be kebab-case")
        if not fm.get("description"):
            error(f"{rel}/SKILL.md: missing 'description'")
        if skill_dir.name not in readme:
            error(f"README.md: skill '{skill_dir.name}' not mentioned")


def main() -> int:
    check_skills(check_manifests())
    if errors:
        for e in errors:
            print(f"error: {e}")
        print(f"\n{len(errors)} error(s)")
        return 1
    print("All checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
