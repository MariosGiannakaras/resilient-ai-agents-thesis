#!/usr/bin/env python3
"""Shared trust-aware catalog loading for the imported bibliography corpus."""
from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from bibliography_import import MATERIAL_ID_RE, SOURCE_ID_RE, BibliographyImportError


@dataclass(frozen=True)
class SourceRecord:
    source_id: str
    title: str
    role: str
    status: str
    topics: str
    trust: str
    citation_ready: bool


@dataclass(frozen=True)
class MaterialRecord:
    material_id: str
    title: str
    confidence: str
    relevance: str
    status: str
    linked_source_id: str


@dataclass(frozen=True)
class CatalogIndex:
    sources: dict[str, SourceRecord]
    materials: dict[str, MaterialRecord]
    citation_ready_ids: frozenset[str]


def _rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            return list(reader.fieldnames or []), [dict(row) for row in reader]
    except (OSError, UnicodeDecodeError, csv.Error) as exc:
        raise BibliographyImportError(f"Cannot read bibliography catalog {path}: {exc}") from exc


def _column(fields: list[str], *names: str) -> str:
    for name in names:
        if name in fields:
            return name
    raise BibliographyImportError(f"Missing expected catalog column: {names}")


def _source_state(role: str, analysis_status: str, citation_ready: bool) -> str:
    if citation_ready:
        return "citation-ready"
    normalized = f"{role} {analysis_status}".casefold()
    if "απορρί" in normalized or "reject" in normalized or role.casefold() == "απόρριψη":
        return "rejected"
    if "θεωρ" in normalized or "theory-only" in normalized or "non-citation theory" in normalized:
        return "theory-only"
    return "canonical-non-citation"


def load_catalog(import_dir: Path) -> CatalogIndex:
    import_dir = import_dir.resolve()
    source_fields, source_rows = _rows(import_dir / "catalog" / "sources.csv")
    source_key = _column(source_fields, "Κωδικός", "Source ID", "source_id")
    title_key = next((name for name in ("Τίτλος", "Title", "title") if name in source_fields), None)
    topics_key = next((name for name in ("Θέματα", "Topics", "topics") if name in source_fields), None)

    manifest_fields, manifest_rows = _rows(import_dir / "citation-ready" / "manifest.csv")
    manifest_key = _column(manifest_fields, "Κωδικός", "Source ID", "source_id")
    citation_ready_ids = frozenset((row.get(manifest_key) or "").strip() for row in manifest_rows)

    status_by_id: dict[str, tuple[str, str]] = {}
    status_path = import_dir / "catalog" / "analysis-status.csv"
    if status_path.exists():
        status_fields, status_rows = _rows(status_path)
        status_key = _column(status_fields, "Κωδικός", "Source ID", "source_id")
        role_key = next((name for name in ("Ρόλος", "Role", "role") if name in status_fields), None)
        analysis_key = next(
            (name for name in ("Κατάσταση ανάλυσης", "Analysis status", "analysis_status") if name in status_fields),
            None,
        )
        for row in status_rows:
            source_id = (row.get(status_key) or "").strip()
            status_by_id[source_id] = (
                (row.get(role_key) or "").strip() if role_key else "",
                (row.get(analysis_key) or "").strip() if analysis_key else "",
            )

    selection_path = import_dir / "catalog" / "thesis-selection.csv"
    selection_by_id: dict[str, tuple[str, str]] = {}
    if selection_path.exists():
        selection_fields, selection_rows = _rows(selection_path)
        selection_key = _column(selection_fields, "Κωδικός", "Source ID", "source_id")
        role_key = next((name for name in ("Ρόλος", "Role", "role") if name in selection_fields), None)
        status_key = next((name for name in ("Κατάσταση", "Status", "status") if name in selection_fields), None)
        for row in selection_rows:
            source_id = (row.get(selection_key) or "").strip()
            selection_by_id[source_id] = (
                (row.get(role_key) or "").strip() if role_key else "",
                (row.get(status_key) or "").strip() if status_key else "",
            )

    sources: dict[str, SourceRecord] = {}
    for row in source_rows:
        source_id = (row.get(source_key) or "").strip()
        if not SOURCE_ID_RE.fullmatch(source_id):
            raise BibliographyImportError(f"Invalid canonical source ID in catalog: {source_id!r}")
        role, analysis_status = status_by_id.get(source_id, selection_by_id.get(source_id, ("", "")))
        if source_id in selection_by_id:
            selected_role, selected_status = selection_by_id[source_id]
            role = selected_role or role
            analysis_status = selected_status or analysis_status
        ready = source_id in citation_ready_ids
        sources[source_id] = SourceRecord(
            source_id=source_id,
            title=(row.get(title_key) or "").strip() if title_key else "",
            role=role,
            status=analysis_status,
            topics=(row.get(topics_key) or "").strip() if topics_key else "",
            trust=_source_state(role, analysis_status, ready),
            citation_ready=ready,
        )

    inventory_fields, inventory_rows = _rows(import_dir / "catalog" / "research-materials.csv")
    inventory_key = _column(inventory_fields, "material_id")
    inventory = {(row.get(inventory_key) or "").strip(): row for row in inventory_rows}
    review_fields, review_rows = _rows(import_dir / "catalog" / "research-material-review.csv")
    review_key = _column(review_fields, "material_id")
    materials: dict[str, MaterialRecord] = {}
    for row in review_rows:
        material_id = (row.get(review_key) or "").strip()
        if not MATERIAL_ID_RE.fullmatch(material_id):
            raise BibliographyImportError(f"Invalid material ID in catalog: {material_id!r}")
        base = inventory.get(material_id, {})
        materials[material_id] = MaterialRecord(
            material_id=material_id,
            title=(row.get("canonical_title") or base.get("title_candidate") or "").strip(),
            confidence=(row.get("confidence") or "").strip(),
            relevance=(row.get("thesis_relevance") or "").strip(),
            status=(row.get("identification_status") or "").strip(),
            linked_source_id=(base.get("linked_source_id") or "").strip(),
        )
    return CatalogIndex(sources=sources, materials=materials, citation_ready_ids=citation_ready_ids)
