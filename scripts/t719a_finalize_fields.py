from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from zipfile import ZIP_DEFLATED, ZipFile
import hashlib
import json

from lxml import etree

DOCX = Path("artifacts/t719a/T719A_targeted_final_pass_review_ready.docx")
QA = Path("artifacts/t719a/T719A_qa-report.json")
TARGET = "5.2.2 Αποτελεσματικότητα μάθησης κατά μήκος του διαθέσιμου προϋπολογισμού"
OLD_PAGE = "57"
NEW_PAGE = "58"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ptext(p: etree._Element) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS))


def style(p: etree._Element) -> str | None:
    vals = p.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
    return vals[0] if vals else None


def main() -> None:
    qa = json.loads(QA.read_text(encoding="utf-8"))
    if qa.get("status") != "docx-static-pass":
        raise RuntimeError("refusing field-cache update before static DOCX QA passes")

    before_sha = sha256(DOCX)
    with ZipFile(DOCX) as zin:
        infos = zin.infolist()
        files = {info.filename: zin.read(info.filename) for info in infos}

    root = etree.fromstring(files["word/document.xml"])
    toc_hits = [
        p
        for p in root.xpath(".//w:body//w:p", namespaces=NS)
        if style(p) == "TOC3" and ptext(p) == TARGET + OLD_PAGE
    ]
    if len(toc_hits) != 1:
        raise RuntimeError(f"expected exactly one stale TOC cache for {TARGET!r}, got {len(toc_hits)}")

    heading_hits = [
        p
        for p in root.xpath(".//w:body//w:p", namespaces=NS)
        if style(p) == "Heading3" and ptext(p) == TARGET
    ]
    if len(heading_hits) != 1:
        raise RuntimeError(f"expected exactly one body heading for {TARGET!r}, got {len(heading_hits)}")

    texts = toc_hits[0].xpath(".//w:t", namespaces=NS)
    if not texts or texts[-1].text != OLD_PAGE:
        raise RuntimeError("TOC cache structure is not the expected final-page text run")
    texts[-1].text = NEW_PAGE

    files["word/document.xml"] = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )

    with NamedTemporaryFile(suffix=".docx", delete=False, dir=DOCX.parent) as tmp:
        tmp_path = Path(tmp.name)
    try:
        with ZipFile(tmp_path, "w", ZIP_DEFLATED) as zout:
            for info in infos:
                zout.writestr(info, files[info.filename])
        tmp_path.replace(DOCX)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    # Structural proof after write.
    with ZipFile(DOCX) as z:
        out_root = etree.fromstring(z.read("word/document.xml"))
    updated = [
        p
        for p in out_root.xpath(".//w:body//w:p", namespaces=NS)
        if style(p) == "TOC3" and ptext(p) == TARGET + NEW_PAGE
    ]
    stale = [
        p
        for p in out_root.xpath(".//w:body//w:p", namespaces=NS)
        if style(p) == "TOC3" and ptext(p) == TARGET + OLD_PAGE
    ]
    if len(updated) != 1 or stale:
        raise RuntimeError("TOC cache update did not converge to exactly one 58 entry")

    qa.update(
        {
            "pre_field_cache_sha256": before_sha,
            "output_raw_sha256": sha256(DOCX),
            "navigation_field_cache_updated": True,
            "toc_cache_updates": {TARGET: {"from": 57, "to": 58}},
            "toc_cache_update_reason": "natural reflow from the accepted RQ1 clarification moved only this body heading by one page",
        }
    )
    QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
