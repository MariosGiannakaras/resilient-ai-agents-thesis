#!/usr/bin/env python3
"""T-711 citation-ready metadata compatibility layer.

The underlying T-711 hardening adapter remains authoritative for composition and
visual-QA fixes. This wrapper broadens only bibliographic-identity parsing across
the two verified citation-ready analysis templates present in the synchronized
corpus:

1. English ``## Bibliographic identity`` followed by a verified prose identity.
2. Greek ``## Βιβλιογραφική ταυτότητα`` with verified structured metadata bullets.

No catalog display title is used as a fallback. Missing verified title/authors/year
continues to fail closed.
"""

from __future__ import annotations

import re

import t711_build_entry as t711


def _strip_md(value: str) -> str:
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\1", value)
    return value.replace("`", "").strip()


def _english_identity(md: str, source_id: str) -> str | None:
    marker = "## Bibliographic identity"
    if marker not in md:
        return None
    tail = md.split(marker, 1)[1].lstrip()
    lines: list[str] = []
    for line in tail.splitlines():
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        if stripped.startswith("#") or stripped.startswith("-"):
            if lines:
                break
            continue
        lines.append(stripped)
    identity = _strip_md(" ".join(lines))
    if len(identity) < 20 or identity.lower().startswith("http") or "https---" in identity or "http---" in identity:
        raise ValueError(f"unsafe verified bibliographic identity for {source_id}: {identity!r}")
    return identity if identity.endswith(".") else identity + "."


def _greek_identity(md: str, source_id: str) -> str | None:
    marker = "## Βιβλιογραφική ταυτότητα"
    if marker not in md:
        return None

    prefix = md.split(marker, 1)[0]
    headings = re.findall(r"^#\s+(.+?)\s*$", prefix, re.MULTILINE)
    if not headings:
        raise ValueError(f"verified title missing for {source_id}")
    title = _strip_md(headings[-1])

    tail = md.split(marker, 1)[1]
    fields: dict[str, str] = {}
    for raw in tail.splitlines():
        stripped = raw.strip()
        if stripped.startswith("## "):
            break
        match = re.match(r"^-\s+\*\*([^*]+):\*\*\s*(.+?)\s*$", stripped)
        if match:
            fields[match.group(1).strip().lower()] = _strip_md(match.group(2))

    authors = fields.get("συγγραφείς") or fields.get("συγγραφέας") or fields.get("authors") or fields.get("author")
    year = fields.get("έτος") or fields.get("year")
    locator = (
        fields.get("doi / arxiv / url")
        or fields.get("doi/url")
        or fields.get("doi")
        or fields.get("url")
        or ""
    ).strip()

    if not title or not authors or not year:
        raise ValueError(
            f"verified structured bibliographic identity incomplete for {source_id}: "
            f"title={bool(title)} authors={bool(authors)} year={bool(year)}"
        )

    identity = f'{authors}, “{title},” {year}.'
    if locator and not locator.startswith("πρωτότυπα/"):
        identity += f" [Online]. Available: {locator}"
    if "https---" in identity or "http---" in identity:
        raise ValueError(f"unsafe verified bibliographic identity for {source_id}: {identity!r}")
    return identity


def _analysis_identity(source_id: str) -> str:
    path = t711.builder.BIB / "analyses" / f"{source_id}.md"
    if not path.exists():
        raise FileNotFoundError(f"citation-ready analysis missing for {source_id}")
    md = path.read_text(encoding="utf-8")
    identity = _english_identity(md, source_id) or _greek_identity(md, source_id)
    if identity is None:
        raise ValueError(f"verified bibliographic identity missing for {source_id}")
    return identity


t711._analysis_identity = _analysis_identity

if __name__ == "__main__":
    t711.builder.main()
