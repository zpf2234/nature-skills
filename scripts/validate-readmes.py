#!/usr/bin/env python3
"""Validate repository README and skill README consistency."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
TOP_READMES = (ROOT / "README.md", ROOT / "README_EN.md")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BADGES_RE = re.compile(r"<img[^>]+src=\"https://img\.shields\.io/badge/[^\"]+\"", re.I)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        fail(f"missing {path.relative_to(ROOT)}")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def skill_dirs() -> list[Path]:
    if not SKILLS_DIR.is_dir():
        fail("skills/ directory not found")
    return sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())


def triggerable_skill_dirs(dirs: list[Path]) -> list[Path]:
    return [path for path in dirs if path.name != "nature-shared"]


def count_skill_index_rows(text: str) -> int:
    try:
        section = text.split("## 6.", 1)[1].split("## 7.", 1)[0]
    except IndexError:
        fail("README is missing the section 6 skill index or section 7 boundary")
    return len(re.findall(r"^\| \[`nature-[^`]+`\]\(", section, flags=re.MULTILINE))


def validate_local_links(path: Path, text: str) -> None:
    """Ensure relative README links point at files committed in this checkout."""
    for match in LINK_RE.finditer(text):
        target = match.group(1).strip()
        if (
            not target
            or target.startswith(("http://", "https://", "mailto:", "#"))
            or "<" in target
            or ">" in target
        ):
            continue
        target = target.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue
        local = (path.parent / target).resolve()
        if not local.exists():
            fail(f"{rel(path)} has broken local link: {match.group(1)}")


def validate_top_readmes(triggerable_count: int) -> None:
    for path in TOP_READMES:
        text = read(path)
        match = re.search(r"skills-(\d+)-0ea5e9", text)
        if not match:
            fail(f"{path.name} is missing the skills-count badge")
        badge_count = int(match.group(1))
        if badge_count != triggerable_count:
            fail(
                f"{path.name} badge says {badge_count}, "
                f"expected {triggerable_count} triggerable skills"
            )
        index_rows = count_skill_index_rows(text)
        if index_rows != triggerable_count:
            fail(
                f"{path.name} skill index has {index_rows} rows, "
                f"expected {triggerable_count}"
            )
        validate_local_links(path, text)
        print(f"ok: {path.name} badge, index count, and local links")


def validate_skill_readmes(dirs: list[Path]) -> None:
    for skill_dir in dirs:
        name = skill_dir.name
        readme = skill_dir / "README.md"
        readme_en = skill_dir / "README_EN.md"
        if not readme.is_file():
            fail(f"{name} is missing README.md")
        if not readme_en.is_file():
            fail(f"{name} is missing README_EN.md")
        validate_local_links(readme, read(readme))
        validate_local_links(readme_en, read(readme_en))
        print(f"ok: {name} includes README.md, README_EN.md, and valid local links")


def main() -> int:
    dirs = skill_dirs()
    validate_top_readmes(len(triggerable_skill_dirs(dirs)))
    validate_skill_readmes(dirs)
    print("README validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
