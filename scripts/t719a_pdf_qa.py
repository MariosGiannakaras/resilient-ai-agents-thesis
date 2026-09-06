from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile
import json
import re
import sys
import unicodedata

from lxml import etree
from pypdf import PdfReader

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def ptext(p: etree._Element) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS))


def norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text or "")
    text = text.replace("\u00a0", " ")
    text = text.replace("‐", "-").replace("‑", "-").replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def pdf_pages(path: Path) -> list[str]:
    reader = PdfReader(str(path))
    return [norm(page.extract_text() or "") for page in reader.pages]


def occurrence_pages(target: str, pages: list[str]) -> tuple[int, ...]:
    t = norm(target)
    if not t:
        return ()
    return tuple(i + 1 for i, page in enumerate(pages) if t in page)


def doc_targets(docx: Path) -> tuple[list[str], list[str]]:
    with ZipFile(docx) as z:
        root = etree.fromstring(z.read("word/document.xml"))
    headings: list[str] = []
    captions: list[str] = []
    for p in root.xpath(".//w:body//w:p", namespaces=NS):
        style = p.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
        style_id = style[0] if style else ""
        text = ptext(p)
        if not text:
            continue
        if style_id in {"Heading1", "Heading2", "Heading3"}:
            headings.append(text)
        instr = " ".join(p.xpath(".//w:instrText/text()", namespaces=NS))
        if "SEQ " in instr:
            captions.append(text)
    return headings, captions


def compare_target_maps(targets: list[str], base_pages: list[str], candidate_pages: list[str]) -> dict:
    unchanged = 0
    missing_base: list[str] = []
    missing_candidate: list[str] = []
    changed: list[dict] = []
    for target in targets:
        b = occurrence_pages(target, base_pages)
        c = occurrence_pages(target, candidate_pages)
        if not b:
            missing_base.append(target)
            continue
        if not c:
            missing_candidate.append(target)
            continue
        if b == c:
            unchanged += 1
        else:
            changed.append({"target": target, "baseline_pages": b, "candidate_pages": c})
    return {
        "target_count": len(targets),
        "unchanged_occurrence_map_count": unchanged,
        "missing_in_baseline_count": len(missing_base),
        "missing_in_candidate_count": len(missing_candidate),
        "changed_occurrence_map_count": len(changed),
        "missing_in_baseline_sample": missing_base[:5],
        "missing_in_candidate_sample": missing_candidate[:5],
        "changed_sample": changed[:5],
    }


def main() -> None:
    if len(sys.argv) != 5:
        raise SystemExit("usage: t719a_pdf_qa.py BASE.docx BASE.pdf CANDIDATE.pdf QA.json")
    base_docx = Path(sys.argv[1])
    base_pdf = Path(sys.argv[2])
    candidate_pdf = Path(sys.argv[3])
    qa_path = Path(sys.argv[4])

    qa = json.loads(qa_path.read_text(encoding="utf-8"))
    if qa.get("status") != "docx-static-pass":
        raise RuntimeError("static DOCX QA did not pass")

    base_pages = pdf_pages(base_pdf)
    candidate_pages = pdf_pages(candidate_pdf)
    headings, captions = doc_targets(base_docx)

    heading_map = compare_target_maps(headings, base_pages, candidate_pages)
    caption_map = compare_target_maps(captions, base_pages, candidate_pages)

    # The T-719 accepted document has 139 cached TOC entries and 27 list-of-figure/table entries.
    # Heading/caption extraction from the body must remain stable enough to prove that the three
    # bounded prose edits did not move any target under the same PDF renderer.
    if len(headings) < 100:
        raise RuntimeError(f"unexpectedly small heading inventory: {len(headings)}")
    if len(captions) != 27:
        raise RuntimeError(f"expected 27 SEQ captions, got {len(captions)}")

    page_count_unchanged = len(base_pages) == len(candidate_pages)
    if not page_count_unchanged:
        raise RuntimeError(f"PDF page count changed: {len(base_pages)} -> {len(candidate_pages)}")

    if heading_map["missing_in_candidate_count"] or heading_map["changed_occurrence_map_count"]:
        raise RuntimeError(f"heading page mapping changed: {heading_map}")
    if caption_map["missing_in_candidate_count"] or caption_map["changed_occurrence_map_count"]:
        raise RuntimeError(f"caption page mapping changed: {caption_map}")

    # Some targets may be absent from baseline PDF text extraction because of field/rendering quirks;
    # those are reported but are not allowed to disappear newly from the candidate.
    if heading_map["missing_in_candidate_count"] > heading_map["missing_in_baseline_count"]:
        raise RuntimeError("new heading extraction loss in candidate PDF")
    if caption_map["missing_in_candidate_count"] > caption_map["missing_in_baseline_count"]:
        raise RuntimeError("new caption extraction loss in candidate PDF")

    base_blank = tuple(i + 1 for i, text in enumerate(base_pages) if not text)
    cand_blank = tuple(i + 1 for i, text in enumerate(candidate_pages) if not text)
    if base_blank != cand_blank:
        raise RuntimeError(f"blank-text PDF page set changed: {base_blank} -> {cand_blank}")

    candidate_text = "\n".join(candidate_pages)
    required_new = (
        "recovery είναι η σταθερή ικανοποίηση του προκαθορισμένου directed AN−AD performance-gap criterion",
        "resource/budget matching",
        "shortest-path επίλυσης του task",
    )
    missing_new = [x for x in required_new if norm(x) not in candidate_text]
    if missing_new:
        raise RuntimeError(f"new targeted text missing from PDF: {missing_new}")
    if norm("stable προσέγγιση της Adaptive-Disturbed trajectory") in candidate_text:
        raise RuntimeError("obsolete symmetric Recovery wording remains in exported PDF")

    # Targeted corruption sentinels for Greek/English mathematical prose.
    pdf_sentinels = (
        "Q-Learning",
        "SARSA",
        "DQN",
        "PPO",
        "Dyna-Q+",
        "FN",
        "FD",
        "AN",
        "AD",
        "8.192",
        "256",
        "0,05",
        "0,10",
        "0,20",
        "right-censored",
        "recovery_time",
    )
    missing_pdf_sentinels = [s for s in pdf_sentinels if norm(s) not in candidate_text]
    if missing_pdf_sentinels:
        raise RuntimeError(f"candidate PDF text corruption/missing sentinel: {missing_pdf_sentinels}")

    qa.update(
        {
            "status": "mechanical-pdf-pass",
            "pdf_qa": "mechanical-pass-pending-final-visual-inspection",
            "pdf_baseline_page_count": len(base_pages),
            "pdf_candidate_page_count": len(candidate_pages),
            "pdf_page_count_unchanged": True,
            "pdf_heading_occurrence_map": heading_map,
            "pdf_caption_occurrence_map": caption_map,
            "pdf_blank_text_pages_baseline": base_blank,
            "pdf_blank_text_pages_candidate": cand_blank,
            "pdf_new_targeted_text_present": True,
            "pdf_obsolete_recovery_wording_absent": True,
            "pdf_text_sentinel_check": "PASS",
        }
    )
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
