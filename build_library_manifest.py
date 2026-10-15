#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генерира Lessons/Other/Library/library/manifest.json от .md файловете в същата папка.

Всеки .md файл може да започне с frontmatter блок:

    ---
    title: Заглавие
    author: Автор
    date: 2026-03-01
    topic: Категория
    tags: таг1, таг2, таг3
    ---
    # Съдържание...

Всички полета са опционални:
  - title  -> fallback: първия "# heading" в тялото на файла, после stem на файлa
  - date   -> fallback: датата на последния git commit върху файла, после file mtime
  - author, topic, tags -> остават празни ("" / []) ако липсват

Пускай ръчно всеки път, когато добавиш/редактираш .md файл в library/:
    python build_library_manifest.py
"""

import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parent
LIBRARY_DIR = BASE / "Lessons" / "Other" / "Library" / "library"
MANIFEST_PATH = LIBRARY_DIR / "manifest.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
HEADING_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


def strip_quotes(value: str):
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def parse_frontmatter(text: str):
    """Връща (fields_dict, body_text)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    fields = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip().lower()] = strip_quotes(value.strip())

    body = text[match.end():]
    return fields, body


def split_list(value: str):
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def git_last_modified(path: Path):
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(path)],
            cwd=BASE, capture_output=True, text=True, check=True,
        )
        iso_date = result.stdout.strip()
        return iso_date[:10] if iso_date else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def file_mtime(path: Path):
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")


def build_entry(md_path: Path):
    text = md_path.read_text(encoding="utf-8")
    fields, body = parse_frontmatter(text)

    title = fields.get("title")
    if not title:
        heading_match = HEADING_RE.search(body)
        title = heading_match.group(1).strip() if heading_match else md_path.stem

    date = fields.get("date") or git_last_modified(md_path) or file_mtime(md_path)

    rel_path = md_path.relative_to(LIBRARY_DIR).as_posix()
    file_rel_to_viewer = f"library/{rel_path}"

    return {
        "id": rel_path,
        "title": title,
        "author": fields.get("author", ""),
        "date": date,
        "topic": fields.get("topic", ""),
        "tags": split_list(fields.get("tags", "")),
        "file": file_rel_to_viewer,
    }


def main():
    if not LIBRARY_DIR.exists():
        print(f"Няма такава папка: {LIBRARY_DIR}")
        return

    entries = [build_entry(p) for p in sorted(LIBRARY_DIR.rglob("*.md"))]
    entries.sort(key=lambda e: e["date"] or "", reverse=True)

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

    print(f"Намерени статии: {len(entries)}")
    print(f"Записан файл: {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
