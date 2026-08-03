#!/usr/bin/env python3
"""Deterministic trust-aware local search over the imported bibliography corpus."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from bibliography_catalog import CatalogIndex, load_catalog
from bibliography_import import BibliographyImportError, validate_installed_package

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMPORT_DIR = ROOT / "research" / "bibliography"
DEFAULT_INDEX = ROOT / ".cache" / "bibliography" / "search-index.json"
SEARCH_LAYERS = ("sources", "analyses", "evidence", "materials", "notes", "aggregates")
ID_RE = re.compile(r"^(?:SRC|MAT)-[A-F0-9]{10}$")


@dataclass(frozen=True)
class SearchDocument:
    identifier: str
    title: str
    layer: str
    role: str
    status: str
    trust: str
    citation_ready: bool
    confidence: str
    relevance: str
    topics: str
    relative_path: str
    content_sha256: str
    text: str


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def _document_for(path: Path, import_dir: Path, layer: str, catalog: CatalogIndex) -> SearchDocument:
    text = path.read_text(encoding="utf-8")
    stem = path.stem
    identifier = stem if ID_RE.fullmatch(stem) else ""
    title = _heading(text)
    role = status = confidence = relevance = topics = ""
    citation_ready = False
    if identifier.startswith("SRC-"):
        record = catalog.sources.get(identifier)
        if record:
            title = record.title or title
            role = record.role
            status = record.status
            topics = record.topics
            trust = record.trust
            citation_ready = record.citation_ready
        else:
            trust = "unknown-source"
    elif identifier.startswith("MAT-"):
        record = catalog.materials.get(identifier)
        if record:
            title = record.title or title
            status = record.status
            confidence = record.confidence
            relevance = record.relevance
        trust = "research-material"
    elif layer == "notes":
        trust = "author-note"
    elif layer == "aggregates":
        trust = "aggregate"
    elif layer == "evidence":
        trust = "non-citation-evidence"
    else:
        trust = "unclassified"
    return SearchDocument(
        identifier=identifier,
        title=title,
        layer=layer,
        role=role,
        status=status,
        trust=trust,
        citation_ready=citation_ready,
        confidence=confidence,
        relevance=relevance,
        topics=topics,
        relative_path=path.relative_to(import_dir).as_posix(),
        content_sha256=_sha256_text(text),
        text=text,
    )


def build_index(import_dir: Path, index_path: Path) -> list[SearchDocument]:
    import_dir = import_dir.resolve()
    validate_installed_package(import_dir)
    catalog = load_catalog(import_dir)
    documents: list[SearchDocument] = []
    for layer in SEARCH_LAYERS:
        root = import_dir / layer
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.md"), key=lambda item: item.relative_to(import_dir).as_posix()):
            documents.append(_document_for(path, import_dir, layer, catalog))
    documents.sort(key=lambda item: (item.relative_path, item.identifier, item.title))
    index_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "source_commit": validate_installed_package(import_dir).corpus_source_commit,
        "documents": [asdict(document) for document in documents],
    }
    index_path.write_text(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return documents


def load_index(import_dir: Path, index_path: Path, rebuild: bool = False) -> list[SearchDocument]:
    if rebuild or not index_path.exists():
        return build_index(import_dir, index_path)
    try:
        payload = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return build_index(import_dir, index_path)
    if payload.get("schema_version") != 1 or not isinstance(payload.get("documents"), list):
        return build_index(import_dir, index_path)
    current = validate_installed_package(import_dir)
    if payload.get("source_commit") != current.corpus_source_commit:
        return build_index(import_dir, index_path)
    try:
        return [SearchDocument(**document) for document in payload["documents"]]
    except (TypeError, KeyError):
        return build_index(import_dir, index_path)


def _snippet(text: str, query: str, width: int = 220) -> str:
    collapsed = " ".join(text.split())
    if not collapsed:
        return ""
    folded = collapsed.casefold()
    needle = query.casefold()
    position = folded.find(needle) if needle else 0
    if position < 0:
        position = 0
    start = max(0, position - width // 3)
    end = min(len(collapsed), start + width)
    prefix = "…" if start else ""
    suffix = "…" if end < len(collapsed) else ""
    return prefix + collapsed[start:end] + suffix


def search_documents(
    documents: list[SearchDocument],
    query: str,
    *,
    identifier: str | None = None,
    layers: set[str] | None = None,
    citation_ready: bool = False,
    include_rejected: bool = False,
    topic: str | None = None,
) -> list[tuple[SearchDocument, str]]:
    query_folded = query.casefold()
    topic_folded = topic.casefold() if topic else ""
    results: list[tuple[SearchDocument, str]] = []
    for document in documents:
        if identifier and document.identifier != identifier:
            continue
        if layers and document.layer not in layers:
            continue
        if citation_ready and not document.citation_ready:
            continue
        if not include_rejected and not identifier and document.trust == "rejected":
            continue
        if topic_folded and topic_folded not in f"{document.topics} {document.title} {document.text}".casefold():
            continue
        haystack = " ".join(
            [document.identifier, document.title, document.role, document.status, document.topics, document.text]
        ).casefold()
        if query_folded and query_folded not in haystack:
            continue
        results.append((document, _snippet(document.text, query or identifier or topic or "")))
    results.sort(key=lambda item: (item[0].relative_path, item[0].identifier))
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="")
    parser.add_argument("--import-dir", type=Path, default=DEFAULT_IMPORT_DIR)
    parser.add_argument("--index", type=Path, default=DEFAULT_INDEX)
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("--citation-ready", action="store_true")
    parser.add_argument("--include-rejected", action="store_true")
    parser.add_argument("--layer", action="append", choices=SEARCH_LAYERS)
    parser.add_argument("--id", dest="identifier")
    parser.add_argument("--topic")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.identifier and not ID_RE.fullmatch(args.identifier):
        parser.error("--id must be a canonical SRC-* or MAT-* identifier")
    try:
        documents = load_index(args.import_dir, args.index, args.rebuild_index)
        results = search_documents(
            documents,
            args.query,
            identifier=args.identifier,
            layers=set(args.layer or []),
            citation_ready=args.citation_ready,
            include_rejected=args.include_rejected,
            topic=args.topic,
        )[: max(args.limit, 0)]
    except BibliographyImportError as exc:
        print(f"Bibliography search failed: {exc}")
        return 1
    if args.json:
        print(json.dumps([
            {**asdict(document), "snippet": snippet} for document, snippet in results
        ], ensure_ascii=False, indent=2))
        return 0
    for document, snippet in results:
        identifier = document.identifier or "(no formal identifier)"
        print(
            f"{identifier} | {document.layer} | trust={document.trust} | "
            f"citation_ready={str(document.citation_ready).lower()} | {document.relative_path}"
        )
        if document.title:
            print(f"  title: {document.title}")
        if document.confidence or document.relevance:
            print(f"  material: confidence={document.confidence or '-'} relevance={document.relevance or '-'}")
        if snippet:
            print(f"  {snippet}")
    print(f"{len(results)} result(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
