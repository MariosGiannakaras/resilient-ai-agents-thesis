from __future__ import annotations

from pathlib import Path
import json
import re
import sys

from pypdf import PdfReader

import t719a_pdf_qa as baseqa

TARGET = "5.2.2 Αποτελεσματικότητα μάθησης κατά μήκος του διαθέσιμου προϋπολογισμού"
EXPECTED_BASE_PAGES = (9, 57)
EXPECTED_CANDIDATE_PAGES = (9, 58)


def main() -> None:
    if len(sys.argv) != 6:
        raise SystemExit(
            "usage: t719a_pdf_qa_final.py BASE.docx BASE.pdf CANDIDATE.docx CANDIDATE.pdf QA.json"
        )
    base_docx = Path(sys.argv[1])
    base_pdf = Path(sys.argv[2])
    candidate_docx = Path(sys.argv[3])
    candidate_pdf = Path(sys.argv[4])
    qa_path = Path(sys.argv[5])

    qa = json.loads(qa_path.read_text(encoding="utf-8"))
    if qa.get("status") != "docx-static-pass":
        raise RuntimeError("static DOCX QA did not pass")
    if qa.get("toc_cache_updates", {}).get(TARGET) != {"from": 57, "to": 58}:
        raise RuntimeError("expected bounded TOC cache update is missing")

    base_pages = baseqa.pdf_pages(base_pdf)
    candidate_pages = baseqa.pdf_pages(candidate_pdf)
    headings, captions = baseqa.doc_targets(base_docx)

    if len(base_pages) != len(candidate_pages):
        raise RuntimeError(f"PDF page count changed: {len(base_pages)} -> {len(candidate_pages)}")
    if len(headings) < 100:
        raise RuntimeError(f"unexpectedly small heading inventory: {len(headings)}")
    if len(captions) != 27:
        raise RuntimeError(f"expected 27 SEQ captions, got {len(captions)}")

    heading_map = baseqa.compare_target_maps(headings, base_pages, candidate_pages)
    caption_map = baseqa.compare_target_maps(captions, base_pages, candidate_pages)

    changed = heading_map["changed_sample"]
    if heading_map["changed_occurrence_map_count"] != 1 or len(changed) != 1:
        raise RuntimeError(f"expected one natural heading reflow, got {heading_map}")
    change = changed[0]
    if (
        change["target"] != TARGET
        or tuple(change["baseline_pages"]) != EXPECTED_BASE_PAGES
        or tuple(change["candidate_pages"]) != EXPECTED_CANDIDATE_PAGES
    ):
        raise RuntimeError(f"unexpected heading movement: {change}")
    if heading_map["missing_in_candidate_count"]:
        raise RuntimeError(f"candidate lost headings: {heading_map}")

    if caption_map["missing_in_candidate_count"] or caption_map["changed_occurrence_map_count"]:
        raise RuntimeError(f"caption page mapping changed: {caption_map}")

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
    missing_new = [x for x in required_new if baseqa.norm(x) not in candidate_text]
    if missing_new:
        raise RuntimeError(f"new targeted text missing from PDF: {missing_new}")
    if baseqa.norm("stable προσέγγιση της Adaptive-Disturbed trajectory") in candidate_text:
        raise RuntimeError("obsolete symmetric Recovery wording remains in exported PDF")

    candidate_reader = PdfReader(str(candidate_pdf))
    toc_raw = candidate_reader.pages[8].extract_text() or ""
    toc_lines = [baseqa.norm(line) for line in toc_raw.splitlines() if TARGET in baseqa.norm(line)]
    if len(toc_lines) != 1 or not re.search(r"\b58\s*$", toc_lines[0]):
        raise RuntimeError(f"TOC cache for {TARGET!r} is not visibly updated to 58: {toc_lines}")

    candidate_doc_headings, candidate_doc_captions = baseqa.doc_targets(candidate_docx)
    if candidate_doc_headings != headings or candidate_doc_captions != captions:
        raise RuntimeError("field-cache finalization unexpectedly altered body heading/caption inventories")

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
    missing_pdf_sentinels = [s for s in pdf_sentinels if baseqa.norm(s) not in candidate_text]
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
            "pdf_expected_natural_reflow": {
                TARGET: {"baseline_body_page": 57, "candidate_body_page": 58}
            },
            "pdf_caption_occurrence_map": caption_map,
            "pdf_blank_text_pages_baseline": base_blank,
            "pdf_blank_text_pages_candidate": cand_blank,
            "pdf_toc_cache_visible_page_58": True,
            "pdf_new_targeted_text_present": True,
            "pdf_obsolete_recovery_wording_absent": True,
            "pdf_text_sentinel_check": "PASS",
        }
    )
    qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
