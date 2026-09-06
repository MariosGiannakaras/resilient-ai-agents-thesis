from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import hashlib
import json
import re

from lxml import etree

BASE = Path("thesis/archive/T719_final_authority_audited_review_ready.docx")
OUT = Path("artifacts/t719a/T719A_targeted_final_pass_review_ready.docx")
QA = Path("artifacts/t719a/T719A_qa-report.json")
BASE_SHA = "1529f2b8a69594f164050544a54e1de115acb40a5a0eb6291156d3ecccf1afb9"

GLOSSARY = Path("docs/thesis/draft/GLOSSARY_ACRONYMS.md")
CH3 = Path("docs/thesis/draft/CHAPTER_03_METHODOLOGY.md")
CH5 = Path("docs/thesis/draft/CHAPTER_05_RESULTS.md")

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
Q = lambda tag: f"{{{W}}}{tag}"

OLD_RECOVERY = (
    "Για το primary RQ3, stable προσέγγιση της Adaptive-Disturbed trajectory στην "
    "Adaptive-Nominal reference σύμφωνα με frozen tolerance και two-window stability rule."
)
NEW_RECOVERY = (
    "Για το primary RQ3, recovery είναι η σταθερή ικανοποίηση του προκαθορισμένου "
    "directed AN−AD performance-gap criterion για δύο συνεχόμενα passive windows."
)

FAIRNESS_ANCHOR = (
    "Οι διαφορές αυτές δεν αντιμετωπίζονται ως αθέμιτες, επειδή αποτελούν μέρος της φυσικής "
    "λειτουργίας κάθε μεθόδου. Το κοινό fairness boundary είναι ότι η εκπαίδευση και η "
    "προσαρμογή μετρώνται με πραγματικές αλληλεπιδράσεις με το ίδιο περιβάλλον. Ο χρόνος "
    "τοίχου, ο CPU time, τα optimizer updates και τα planning updates καταγράφονται ως "
    "δευτερεύοντα περιγραφικά στοιχεία, όχι ως κύριο επιστημονικό budget."
)
FAIRNESS_SENTENCE = (
    "Το κοινό Phase-A interaction budget εξασφαλίζει resource/budget matching μεταξύ των "
    "methods, όχι ισότητα του ονομαστικού επιπέδου επίδοσης που έχει επιτύχει κάθε μέθοδος "
    "στο Phase-B boundary."
)

RQ1_ANCHOR = (
    "Στο τελικό probe των 8.192 interactions, οι Q-Learning, SARSA και Dyna-Q+ κατέληξαν "
    "στην ίδια root-mean επίδοση, -0,100. Και για τις τρεις μεθόδους δεν παρατηρήθηκε "
    "μεταξύ-root διακύμανση στο τελικό probe: n=12 και 95% CI [-0,100, -0,100]."
)
RQ1_EXPLANATION = (
    "Με μήκος βέλτιστης διαδρομής 12 ενεργειών και το frozen reward contract, η τιμή "
    "−0,100 αντιστοιχεί στην απόδοση μιας shortest-path επίλυσης του task: "
    "11×(−0,1)+1,0=−0,1, επειδή η terminal goal reward αντικαθιστά την ordinary step reward "
    "στην τελευταία μετάβαση."
)

FROZEN_SENTINELS = (
    "6,623 [3,798, 9,448]",
    "26,102 [25,344, 26,860]",
    "32,269 [28,910, 35,628]",
    "31,127 [28,796, 33,458]",
    "22,665 [18,078, 27,251]",
    "13,785 [9,904, 17,667]",
    "-2,698 [-3,880, -1,516]",
    "-3,165 [-4,917, -1,412]",
    "[-529,9, 689,9]",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def ptext(p: etree._Element) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS))


def set_p_text(p: etree._Element, text: str) -> None:
    first = next(
        (r for r in p.xpath("./w:r", namespaces=NS) if r.xpath(".//w:t", namespaces=NS)),
        None,
    )
    rpr = (
        deepcopy(first.find("w:rPr", namespaces=NS))
        if first is not None and first.find("w:rPr", namespaces=NS) is not None
        else None
    )
    ppr = p.find("w:pPr", namespaces=NS)
    for child in list(p):
        if child is not ppr:
            p.remove(child)
    run = etree.SubElement(p, Q("r"))
    if rpr is not None:
        run.append(rpr)
    t = etree.SubElement(run, Q("t"))
    t.text = text


def find_exact(root: etree._Element, text: str) -> etree._Element:
    hits = [p for p in root.xpath(".//w:p", namespaces=NS) if ptext(p) == text]
    if len(hits) != 1:
        sample = [ptext(p) for p in root.xpath(".//w:p", namespaces=NS) if text[:35] in ptext(p)]
        raise RuntimeError(f"expected one paragraph anchor, got {len(hits)} for {text!r}; candidates={sample[:4]!r}")
    return hits[0]


def insert_after(anchor: etree._Element, text: str) -> etree._Element:
    newp = deepcopy(anchor)
    set_p_text(newp, text)
    anchor.addnext(newp)
    return newp


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{path}: expected one source anchor, got {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def bibliography_entries(root: etree._Element) -> list[str]:
    entries: list[str] = []
    started = False
    for p in root.xpath(".//w:body//w:p", namespaces=NS):
        text = ptext(p)
        if text == "Βιβλιογραφία":
            started = True
            continue
        if not started:
            continue
        if re.match(r"^\[\d+\]\s", text):
            entries.append(text)
            if len(entries) == 32:
                break
        elif entries:
            break
    if len(entries) != 32:
        raise RuntimeError(f"expected 32 bibliography entries, got {len(entries)}")
    return entries


def citation_sequence_before_bibliography(root: etree._Element) -> list[str]:
    seq: list[str] = []
    for p in root.xpath(".//w:body//w:p", namespaces=NS):
        text = ptext(p)
        if text == "Βιβλιογραφία":
            break
        seq.extend(re.findall(r"\[(?:\d+)(?:\s*[–-]\s*\d+)?\]", text))
    return seq


def section_properties(root: etree._Element) -> list[bytes]:
    return [etree.tostring(x) for x in root.xpath(".//w:sectPr", namespaces=NS)]


def paragraph_style(p: etree._Element) -> str | None:
    vals = p.xpath("./w:pPr/w:pStyle/@w:val", namespaces=NS)
    return vals[0] if vals else None


def expected_targeted_text_sequence(base_root: etree._Element) -> list[str]:
    expected: list[str] = []
    for p in base_root.xpath(".//w:body//w:p", namespaces=NS):
        text = ptext(p)
        if text == OLD_RECOVERY:
            expected.append(NEW_RECOVERY)
        else:
            expected.append(text)
        if text == FAIRNESS_ANCHOR:
            expected.append(FAIRNESS_SENTENCE)
        if text == RQ1_ANCHOR:
            expected.append(RQ1_EXPLANATION)
    return expected


def main() -> None:
    if sha256_path(BASE) != BASE_SHA:
        raise RuntimeError("T-719 base hash mismatch; refusing to patch a different manuscript")

    # Keep the durable editable prose sources aligned with the accepted DOCX changes.
    replace_once(GLOSSARY, OLD_RECOVERY, NEW_RECOVERY)
    replace_once(CH3, FAIRNESS_ANCHOR, FAIRNESS_ANCHOR + "\n\n" + FAIRNESS_SENTENCE)
    replace_once(CH5, RQ1_ANCHOR, RQ1_ANCHOR + "\n\n" + RQ1_EXPLANATION)

    with ZipFile(BASE) as zin:
        infos = zin.infolist()
        base_files = {info.filename: zin.read(info.filename) for info in infos}

    base_root = etree.fromstring(base_files["word/document.xml"])
    root = deepcopy(base_root)

    base_bibliography = bibliography_entries(base_root)
    base_citations = citation_sequence_before_bibliography(base_root)
    base_sections = section_properties(base_root)

    recovery_p = find_exact(root, OLD_RECOVERY)
    recovery_style = paragraph_style(recovery_p)
    set_p_text(recovery_p, NEW_RECOVERY)

    fairness_p = find_exact(root, FAIRNESS_ANCHOR)
    fairness_new = insert_after(fairness_p, FAIRNESS_SENTENCE)
    if paragraph_style(fairness_new) != paragraph_style(fairness_p):
        raise RuntimeError("fairness insertion changed paragraph style")

    rq1_p = find_exact(root, RQ1_ANCHOR)
    rq1_new = insert_after(rq1_p, RQ1_EXPLANATION)
    if paragraph_style(rq1_new) != paragraph_style(rq1_p):
        raise RuntimeError("RQ1 insertion changed paragraph style")

    # Exact semantic delta guard: every body paragraph must be byte-for-text identical to T-719,
    # except the one approved Recovery replacement and the two approved insertions.
    all_texts = [ptext(p) for p in root.xpath(".//w:body//w:p", namespaces=NS)]
    expected_texts = expected_targeted_text_sequence(base_root)
    if all_texts != expected_texts:
        for i, (expected, actual) in enumerate(zip(expected_texts, all_texts, strict=False)):
            if expected != actual:
                raise RuntimeError(
                    f"unexpected paragraph-text delta at index {i}: expected={expected!r} actual={actual!r}"
                )
        raise RuntimeError(
            f"unexpected paragraph sequence length delta: expected={len(expected_texts)} actual={len(all_texts)}"
        )

    for expected in (NEW_RECOVERY, FAIRNESS_SENTENCE, RQ1_EXPLANATION):
        if all_texts.count(expected) != 1:
            raise RuntimeError(f"targeted text count mismatch for {expected!r}")
    if OLD_RECOVERY in all_texts:
        raise RuntimeError("obsolete symmetric Recovery wording remains in manuscript")

    out_files = dict(base_files)
    out_files["word/document.xml"] = etree.tostring(
        root, xml_declaration=True, encoding="UTF-8", standalone="yes"
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT, "w", ZIP_DEFLATED) as zout:
        for info in infos:
            zout.writestr(info, out_files[info.filename])

    # Package-level immutability guards.
    with ZipFile(OUT) as zout:
        output_files = {name: zout.read(name) for name in zout.namelist()}

    changed_entries = sorted(name for name in base_files if base_files[name] != output_files[name])
    if changed_entries != ["word/document.xml"]:
        raise RuntimeError(f"unexpected OOXML changes: {changed_entries}")

    media = sorted(name for name in base_files if name.startswith("word/media/"))
    if len(media) != 25:
        raise RuntimeError(f"unexpected media inventory: {len(media)}")
    if any(base_files[name] != output_files[name] for name in media):
        raise RuntimeError("registered/embedded media changed")

    for prefix in ("word/header", "word/footer"):
        for name in (n for n in base_files if n.startswith(prefix)):
            if base_files[name] != output_files[name]:
                raise RuntimeError(f"header/footer changed unexpectedly: {name}")

    if section_properties(root) != base_sections:
        raise RuntimeError("section/page-numbering properties changed unexpectedly")

    if bibliography_entries(root) != base_bibliography:
        raise RuntimeError("bibliography text/identity/order changed")
    if citation_sequence_before_bibliography(root) != base_citations:
        raise RuntimeError("citation sequence changed")

    if root.xpath(".//w:ins|.//w:del", namespaces=NS):
        raise RuntimeError("tracked changes found")

    manuscript_text = "\n".join(all_texts)
    missing = [x for x in FROZEN_SENTINELS if x not in manuscript_text]
    if missing:
        raise RuntimeError(f"frozen numerical result sentinel missing: {missing}")

    qa = {
        "status": "docx-static-pass",
        "base_raw_sha256": BASE_SHA,
        "output_raw_sha256": sha256_path(OUT),
        "changed_ooxml_entries": changed_entries,
        "paragraph_text_delta_exact": True,
        "semantic_edits": [
            "glossary-directed-recovery-definition",
            "phase-a-budget-matched-not-competence-matched-clarification",
            "rq1-minus-0.100-shortest-path-interpretation",
        ],
        "scientific_results_modified": False,
        "protocol_or_estimand_modified": False,
        "new_experiment_or_reanalysis": False,
        "registered_quantitative_assets_modified": False,
        "media_count": len(media),
        "unchanged_media_count": len(media),
        "bibliography_entry_count": len(base_bibliography),
        "bibliography_unchanged": True,
        "citation_sequence_unchanged": True,
        "headers_footers_unchanged": True,
        "section_page_numbering_properties_unchanged": True,
        "cover_page_numbering_changed": False,
        "appendix_b3_manual_pagination_change": False,
        "front_matter_personal_metadata_changed": False,
        "declaration_text_changed": False,
        "chacon_chamorro_manuscript_identity_changed": False,
        "glossary_previous_style": recovery_style,
        "word_math_semantics": "inherited byte-for-byte from exact T-719 base outside the three approved paragraph deltas",
        "pdf_qa": "pending-workflow-render",
    }
    QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
