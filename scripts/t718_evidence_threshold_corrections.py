#!/usr/bin/env python3
"""Apply only evidence-threshold reader-facing corrections to accepted T-717.

Scientific boundary: no experiment execution/re-analysis; protocol-v2.1, T-611,
T-612 and T-613 quantitative assets remain immutable. The T-717 baseline keeps
all 25 media; only explanatory image1 is regenerated to rename ambiguous
"Held-out layout" labels to "Final layout".
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import tempfile
import zipfile
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASE = ROOT / "thesis/archive/T717_pre_freeze_content_refined_review_ready.docx"
DEFAULT_OUT = ROOT / "artifacts/t718/T718_evidence_threshold_corrected_review_ready.docx"
DEFAULT_QA = ROOT / "artifacts/t718/T718_qa-report.json"
EXPECTED_BASE_SHA256 = "57d6de352eef6147fa24179f87a3f8e9ee39f65a90ad8b85777cac8f541f57c5"
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ptext(p) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS))


def paragraphs(root):
    return root.xpath(".//w:body/w:p", namespaces=NS)


def _preserve_space(node) -> None:
    text = node.text or ""
    if text.startswith(" ") or text.endswith(" "):
        node.set(XML_SPACE, "preserve")
    elif XML_SPACE in node.attrib:
        del node.attrib[XML_SPACE]


def replace_inline(root, old: str, new: str, expected: int = 1) -> int:
    """Replace one exact substring across w:t nodes while preserving surrounding runs."""
    hits = []
    for p in paragraphs(root):
        nodes = p.xpath(".//w:t", namespaces=NS)
        joined = "".join((n.text or "") for n in nodes)
        start = joined.find(old)
        if start >= 0:
            if joined.find(old, start + 1) >= 0:
                raise RuntimeError(f"substring repeats within one paragraph: {old!r}")
            hits.append((p, nodes, start, start + len(old)))
    if len(hits) != expected:
        raise RuntimeError(f"expected {expected} occurrence(s) of {old!r}, found {len(hits)}")

    for _p, nodes, start, end in hits:
        cursor = 0
        first_i = last_i = None
        first_off = last_off = None
        for i, n in enumerate(nodes):
            text = n.text or ""
            nxt = cursor + len(text)
            if first_i is None and start < nxt:
                first_i = i
                first_off = start - cursor
            if end <= nxt:
                last_i = i
                last_off = end - cursor
                break
            cursor = nxt
        if first_i is None or last_i is None:
            raise RuntimeError(f"failed to map replacement range for {old!r}")
        first = nodes[first_i]
        last = nodes[last_i]
        first_text = first.text or ""
        last_text = last.text or ""
        prefix = first_text[:first_off]
        suffix = last_text[last_off:]
        if first_i == last_i:
            first.text = prefix + new + suffix
            _preserve_space(first)
        else:
            first.text = prefix + new
            _preserve_space(first)
            for i in range(first_i + 1, last_i):
                nodes[i].text = ""
                _preserve_space(nodes[i])
            last.text = suffix
            _preserve_space(last)
    return len(hits)


def find_paragraph(root, *, exact: str | None = None, prefix: str | None = None):
    hits = []
    for p in paragraphs(root):
        text = ptext(p)
        if exact is not None and text == exact:
            hits.append(p)
        elif prefix is not None and text.startswith(prefix):
            hits.append(p)
    if len(hits) != 1:
        raise RuntimeError(f"expected one paragraph exact={exact!r} prefix={prefix!r}, found {len(hits)}")
    return hits[0]


def insert_after(anchor, text: str) -> None:
    p = etree.Element(f"{{{W}}}p")
    ppr = anchor.find(f"{{{W}}}pPr")
    if ppr is not None:
        p.append(copy.deepcopy(ppr))
    r = etree.SubElement(p, f"{{{W}}}r")
    t = etree.SubElement(r, f"{{{W}}}t")
    t.text = text
    _preserve_space(t)
    parent = anchor.getparent()
    parent.insert(parent.index(anchor) + 1, p)


def patch_document_xml(xml_bytes: bytes) -> tuple[bytes, dict]:
    root = etree.fromstring(xml_bytes, etree.XMLParser(remove_blank_text=False))
    changes = {}

    # C1 — operational definition of the existing frozen RQ2 scalar.
    old = "Για το RQ2 χρησιμοποιείται το Phase-B return_sum."
    new = (
        "Για το RQ2, κάθε matched τιμή FN/FD/AN/AD είναι το Phase-B return_sum: "
        "το μη προεξοφλημένο αθροιστικό task reward στις σταθερές 256 πραγματικές "
        "αλληλεπιδράσεις μετά το branch boundary. Το άθροισμα συνεχίζεται across "
        "episode boundaries και δεν επαναμηδενίζεται όταν το περιβάλλον κάνει reset "
        "μεταξύ επεισοδίων."
    )
    changes["rq2_return_sum_definition"] = replace_inline(root, old, new)

    # C2 — Frozen means no learning-state updates, not deterministic action selection.
    changes["frozen_stable_policy_phrase"] = replace_inline(
        root,
        "υπό σταθερή πολιτική",
        "με παγωμένο το επιστημονικό learning state",
    )
    frozen_anchor = find_paragraph(
        root,
        prefix="Οι όροι Frozen και Adaptive δεν δηλώνουν διαφορετικούς αλγορίθμους.",
    )
    insert_after(
        frozen_anchor,
        "Το Frozen δεν σημαίνει deterministic action selection: οι ενημερώσεις του learning state "
        "είναι απενεργοποιημένες, αλλά η method-native behavior/inference stochasticity και το "
        "αντίστοιχο RNG state μπορούν να συνεχίσουν να εξελίσσονται. Αντίθετα, τα standardized "
        "Phase-A no-learning probes αποτελούν ξεχωριστή deterministic/greedy evidence surface.",
    )
    changes["frozen_action_selection_note"] = 1

    # C3 — reserve-vs-test terminology.
    old_first = (
        "Η τελική εργασία χρησιμοποιεί δύο held-out διατάξεις 7×7, τις "
        "`gw-l1-final-a` και `gw-l1-final-b`."
    )
    new_first = (
        "Η τελική εργασία χρησιμοποιεί δύο τελικές διατάξεις 7×7, τις "
        "`gw-l1-final-a` και `gw-l1-final-b`. Οι διατάξεις αυτές κρατήθηκαν εκτός "
        "development/tuning μέχρι το άνοιγμα του final reserve και στη συνέχεια "
        "χρησιμοποιήθηκαν στην τελική πειραματική καμπάνια."
    )
    changes["final_layout_first_use"] = replace_inline(root, old_first, new_first)
    # Appendix source wording survives composition in current baseline.
    appendix_old = "δύο held-out final 7×7 layouts"
    appendix_count = sum(appendix_old in ptext(p) for p in paragraphs(root))
    if appendix_count:
        changes["appendix_final_layout_term"] = replace_inline(
            root, appendix_old, "δύο final 7×7 layouts", expected=appendix_count
        )
    else:
        changes["appendix_final_layout_term"] = 0

    # C4 — do not generalize one tested observation-corruption mechanism to observation noise as a class.
    old_clause = (
        "αλλά μπορεί να μην προσφέρει όφελος ή ακόμη και να επιδεινώσει την επίδοση όταν το "
        "learning signal αλλοιώνεται από θόρυβο παρατήρησης."
    )
    new_clause = (
        "ενώ στο συγκεκριμένο observation-corruption-0.05 mechanism η Q-Learning και η SARSA "
        "παρουσίασαν αρνητικό adaptation benefit στο προδηλωμένο RQ2 estimand. Το αποτέλεσμα "
        "αυτό δεν γενικεύεται σε θόρυβο παρατήρησης ως κατηγορία."
    )
    changes["condition_specific_conclusion"] = replace_inline(root, old_clause, new_clause)

    # C5 — ordinary Student-t interval is not physically support constrained.
    ci_anchor = find_paragraph(
        root,
        prefix="Η DQN είχε conditional recovery time 80,0 interactions, αλλά μόνο n=2 recovered roots",
    )
    insert_after(
        ci_anchor,
        "Το πολύ ευρύ Student-t interval με n=2 δεν είναι περιορισμένο από το φυσικό support "
        "0–256 interactions· τα endpoints εκφράζουν sampling uncertainty της προκαθορισμένης "
        "ordinary Student-t summary και δεν αποτελούν φυσικά δυνατούς recovery times. Για αυτό "
        "η ερμηνεία παραμένει δεμένη με το recovered n και το right-censoring.",
    )
    changes["recovery_ci_support_note"] = 1

    # C6 — exact immutable accepted execution identity, separated from UI overlay.
    appendix_heading = find_paragraph(root, exact="Παράρτημα Ε — Αναπαραγωγή και λογισμικό περιβάλλον")
    insert_after(
        appendix_heading,
        "Η accepted final scientific execution είναι η replacement Study "
        "protocol-v2.1-final--t610-recovery-01 από source commit "
        "86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730, σε Windows 10.0.19045 και CPython "
        "3.12.13, με clean tracked και non-output untracked source state όπως καταγράφεται στο "
        "final Study manifest. Η scientific recipe έχει SHA-256 "
        "8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154 και το deterministic "
        "plan SHA-256 073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4. "
        "Το locked scientific environment χρησιμοποιεί Gymnasium 1.3.0, Stable-Baselines3 2.9.0 "
        "και Torch 2.9.0. Η PySide6 6.11.2 είναι ξεχωριστό presentation/UI overlay και δεν "
        "αποτελεί μέρος της επιστημονικής execution identity.",
    )
    changes["execution_identity_note"] = 1

    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes"), changes


def generate_figure1(path: Path) -> None:
    """Reproduce T-717 explanatory Figure 1, changing only layout labels."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Rectangle

    fig = plt.figure(figsize=(9.845, 8.141), dpi=220)
    fig.suptitle("Τελικό GridWorld και παγωμένοι μηχανισμοί διαταραχής", fontsize=18, y=.985)
    layouts = [
        ("Final layout A · seed 57001\n7×7 · shortest path 12 · max_steps 48", [(0,5),(1,2),(1,4),(3,5),(4,0),(5,4),(6,0),(6,3),(6,4)]),
        ("Final layout B · seed 57002\n7×7 · shortest path 12 · max_steps 48", [(0,5),(2,3),(2,4),(2,5),(3,0),(3,2),(3,5),(3,6),(4,6)]),
    ]
    for (title, obs), pos in zip(layouts, [(.09,.52,.30,.33),(.59,.52,.30,.33)]):
        ax = fig.add_axes(pos)
        ax.set_xlim(-.5, 6.5)
        ax.set_ylim(-.5, 6.5)
        ax.set_aspect("equal")
        ax.set_xticks(range(7))
        ax.set_yticks(range(7))
        ax.grid(True, linewidth=.5, alpha=.35)
        for x, y in obs:
            ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor="0.22",edgecolor="0.22"))
        for x, y, label in [(0,0,"S"),(6,6,"G")]:
            ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor="0.88",edgecolor="0.55"))
            ax.text(x,y,label,ha="center",va="center",fontsize=14,fontweight="bold")
        ax.set_title(title, fontsize=11, pad=6)
        ax.set_xlabel("x")
        ax.set_ylabel("y", rotation=0, labelpad=8)
        for spine in ax.spines.values():
            spine.set_alpha(.35)
    cards = [
        ("Swap right/down",["up → up","right → down","down → right","left → left"],"persistent · unannounced"),
        ("Clockwise cycle",["up → right","right → down","down → left","left → up"],"persistent · unannounced"),
        ("Action failure",["intended aₜ","p=.15 → no-op","true state unchanged","reward −0.1"],"executed action hidden"),
        ("Observation corruption",["transition first","p=.05 → false observation","uniform valid support","reward/transition unchanged"],"true state excluded"),
    ]
    for x, (head, lines, foot) in zip([.012,.272,.532,.792], cards):
        ax = fig.add_axes((x,.14,.196,.22))
        ax.set_axis_off()
        ax.add_patch(FancyBboxPatch((.02,.02),.96,.96,boxstyle="round,pad=.015",linewidth=1,facecolor="white",edgecolor="0.25"))
        ax.text(.5,.85,head,ha="center",va="center",fontsize=10.2,fontweight="bold")
        for y, text in zip([.65,.50,.35,.20], lines):
            ax.text(.5,y,text,ha="center",va="center",fontsize=9.1)
        ax.text(.5,.07,foot,ha="center",va="center",fontsize=8.2,fontstyle="italic",color="0.35")
    fig.text(.5,.045,"Τα p=.15 και p=.05 είναι συγκεκριμένα frozen severity points του protocol-v2.1, όχι severity sweep.",ha="center",fontsize=9.5)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def visible_text(xml: bytes) -> str:
    root = etree.fromstring(xml)
    return "\n".join(ptext(p) for p in paragraphs(root))


def build(base: Path, out: Path, qa_path: Path) -> dict:
    if not base.is_file():
        raise FileNotFoundError(base)
    base_sha = sha256_file(base)
    if base_sha != EXPECTED_BASE_SHA256:
        raise RuntimeError(f"unexpected T-717 baseline sha256: {base_sha}")

    with tempfile.TemporaryDirectory(prefix="t718-") as td:
        figure1 = Path(td) / "image1.png"
        generate_figure1(figure1)
        new_image1 = figure1.read_bytes()

        with zipfile.ZipFile(base, "r") as zin:
            infos = zin.infolist()
            payload = {i.filename: zin.read(i.filename) for i in infos}
        required = {"word/document.xml", "word/media/image1.png", "word/media/image2.png"}
        if not required.issubset(payload):
            raise RuntimeError("T-717 package layout changed unexpectedly")

        old_xml = payload["word/document.xml"]
        old_image1 = payload["word/media/image1.png"]
        old_image2 = payload["word/media/image2.png"]
        new_xml, change_counts = patch_document_xml(old_xml)
        payload["word/document.xml"] = new_xml
        payload["word/media/image1.png"] = new_image1

        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, "w") as zout:
            for info in infos:
                zout.writestr(info, payload[info.filename])

    with zipfile.ZipFile(base, "r") as zb, zipfile.ZipFile(out, "r") as zo:
        names_b = zb.namelist()
        names_o = zo.namelist()
        if names_b != names_o:
            raise RuntimeError("OOXML entry set/order changed")
        changed_entries = [n for n in names_b if zb.read(n) != zo.read(n)]
        if changed_entries != ["word/document.xml", "word/media/image1.png"]:
            raise RuntimeError(f"unexpected OOXML changes: {changed_entries}")
        media = [n for n in names_o if n.startswith("word/media/")]
        unchanged_media = [n for n in media if zb.read(n) == zo.read(n)]
        text = visible_text(zo.read("word/document.xml"))
        held_out_lines = [line for line in text.splitlines() if "held-out" in line.lower()]
        result = {
            "status": "pass",
            "base": str(base),
            "output": str(out),
            "base_raw_sha256": sha256_file(base),
            "output_raw_sha256": sha256_file(out),
            "changed_ooxml_entries": changed_entries,
            "change_counts": change_counts,
            "media_count": len(media),
            "unchanged_media_count": len(unchanged_media),
            "image1_changed": zb.read("word/media/image1.png") != zo.read("word/media/image1.png"),
            "image2_preserved": zb.read("word/media/image2.png") == zo.read("word/media/image2.png"),
            "remaining_held_out_paragraphs": held_out_lines,
            "scientific_results_modified": False,
            "new_experiment_or_reanalysis": False,
            "protocol_or_estimand_modified": False,
            "visual_removed": False,
        }

    qa_path.parent.mkdir(parents=True, exist_ok=True)
    qa_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--qa", type=Path, default=DEFAULT_QA)
    args = parser.parse_args()
    report = build(args.base, args.out, args.qa)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
