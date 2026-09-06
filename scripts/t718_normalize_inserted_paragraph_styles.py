#!/usr/bin/env python3
"""Normalize the C6 inserted paragraph to the surrounding body-text paragraph style.

This is a layout-only post-step after the deterministic T-718 content builder.
It copies the pPr from the immediately following canonical appendix body paragraph,
then refreshes the QA output hash. No visible text or media bytes are changed.
"""
from __future__ import annotations

import copy
import hashlib
import json
import zipfile
from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "artifacts/t718/T718_evidence_threshold_corrected_review_ready.docx"
QA = ROOT / "artifacts/t718/T718_qa-report.json"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
PREFIX = "Η accepted final scientific execution είναι η replacement Study protocol-v2.1-final--t610-recovery-01"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ptext(p) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS))


def main() -> None:
    with zipfile.ZipFile(DOCX, "r") as zin:
        infos = zin.infolist()
        payload = {i.filename: zin.read(i.filename) for i in infos}
    root = etree.fromstring(payload["word/document.xml"], etree.XMLParser(remove_blank_text=False))
    matches = [p for p in root.xpath(".//w:body/w:p", namespaces=NS) if ptext(p).startswith(PREFIX)]
    if len(matches) != 1:
        raise RuntimeError(f"expected one C6 paragraph, found {len(matches)}")
    p = matches[0]
    nxt = p.getnext()
    while nxt is not None and nxt.tag != f"{{{W}}}p":
        nxt = nxt.getnext()
    if nxt is None:
        raise RuntimeError("C6 paragraph has no following canonical body paragraph")
    next_ppr = nxt.find(f"{{{W}}}pPr")
    if next_ppr is None:
        raise RuntimeError("following canonical body paragraph has no pPr")
    old_ppr = p.find(f"{{{W}}}pPr")
    if old_ppr is not None:
        p.remove(old_ppr)
    p.insert(0, copy.deepcopy(next_ppr))
    payload["word/document.xml"] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

    tmp = DOCX.with_suffix(".tmp.docx")
    with zipfile.ZipFile(tmp, "w") as zout:
        for info in infos:
            zout.writestr(info, payload[info.filename])
    tmp.replace(DOCX)

    report = json.loads(QA.read_text(encoding="utf-8"))
    report["output_raw_sha256"] = sha256(DOCX)
    report["C6_body_style_normalized"] = True
    QA.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(report["output_raw_sha256"])


if __name__ == "__main__":
    main()
