#!/usr/bin/env python3
"""Export a four-file thesis rewrite workbook from the validated T-715 text ledger.

The workbook is deliberately human-oriented: only four Markdown files, no auxiliary
indexes. It keeps full original-language source Markdown next to every thesis block that
cites the source, then separates uncited theory, project methodology/implementation, and
results/discussion/conclusions for line-by-line student review.

This exporter does not change the thesis, citations, experiment, or scientific results.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "research" / "bibliography" / "sources"

parser = argparse.ArgumentParser()
parser.add_argument("--ledger", type=Path, required=True)
parser.add_argument("--qa", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()

out = args.output.resolve()
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

qa = json.loads(args.qa.read_text(encoding="utf-8"))
with args.ledger.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

citation_map = {str(k): int(v) for k, v in qa["citation_map"].items()}
num_to_sid = {number: sid for sid, number in citation_map.items()}


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def is_heading(row: dict[str, str]) -> bool:
    return (row.get("style") or "").startswith("Heading")


def is_generated_list_cache(row: dict[str, str]) -> bool:
    return (row.get("section") or "") in {
        "Πίνακας Περιεχομένων", "Κατάλογος Σχημάτων", "Κατάλογος Πινάκων"
    }


def blank_editor() -> str:
    return (
        "\n### Η δική μου τελική έκδοση\n\n"
        "<!-- Γράψε εδώ τη δική σου εκδοχή αφού ελέγξεις/καταλάβεις το παραπάνω υλικό. -->\n\n\n\n---\n"
    )


def block(row: dict[str, str]) -> str:
    text = (row.get("text") or "").strip()
    section = row.get("section") or row.get("major") or ""
    ids = split_ids(row.get("source_ids") or "")
    meta = [f"**Θέση στην πτυχιακή:** {row.get('major','')} → {section}"]
    if ids:
        refs = []
        for sid in ids:
            n = citation_map.get(sid)
            refs.append(f"[{n}] `{sid}`" if n else f"`{sid}`")
        meta.append("**Παραπομπές αυτού του κομματιού:** " + ", ".join(refs))
    else:
        meta.append("**Άμεση εξωτερική παραπομπή:** καμία στο συγκεκριμένο κομμάτι")
    return (
        f"## {row['id']}\n\n" + "  \n".join(meta)
        + "\n\n### Κείμενο που υπάρχει τώρα στην πτυχιακή\n\n"
        + text + "\n" + blank_editor()
    )


# Exact reader-visible bibliography entries.
bib_entry: dict[int, str] = {}
for row in rows:
    if row.get("major") != "Βιβλιογραφία":
        continue
    m = re.match(r"^\[(\d+)\]\s+(.*)$", (row.get("text") or "").strip(), re.S)
    if m:
        bib_entry[int(m.group(1))] = m.group(2).strip()


# 01 — Full original-language sources + every reader-visible block using each source.
source_usage: dict[str, list[dict[str, str]]] = defaultdict(list)
for row in rows:
    if is_heading(row) or is_generated_list_cache(row):
        continue
    for sid in split_ids(row.get("source_ids") or ""):
        source_usage[sid].append(row)

parts = [
    "# 01 — Πηγές: ολόκληρο αρχικό κείμενο + τι γράφτηκε στην πτυχιακή\n",
    "Σε κάθε πηγή βλέπεις πρώτα το **πλήρες Markdown που έχει αποθηκευτεί στο bibliography corpus στην αρχική του γλώσσα**, χωρίς μετάφραση ή περίληψη από αυτό το αρχείο. Αμέσως μετά βρίσκονται όλα τα κομμάτια της τρέχουσας πτυχιακής που παραπέμπουν σε αυτή την πηγή και χώρος για τη δική σου τελική διατύπωση.\n",
    "Αν μία παράγραφος στηρίζεται σε περισσότερες από μία πηγές, επαναλαμβάνεται κάτω από καθεμία επίτηδες, ώστε να μη χρειάζεται να ψάχνεις αλλού.\n",
]
for number in sorted(num_to_sid):
    sid = num_to_sid[number]
    source_path = SOURCES / f"{sid}.md"
    entry = bib_entry.get(number, "")
    parts.append(f"\n# [{number}] {sid}\n")
    if entry:
        parts.append(f"**Βιβλιογραφική εγγραφή:** {entry}\n")
    parts.append("\n## Α. Αρχικό κείμενο πηγής — χωρίς μετάφραση\n")
    if source_path.exists():
        original = source_path.read_text(encoding="utf-8", errors="replace").strip()
        if original:
            parts.append("\n" + original + "\n")
        else:
            parts.append("\n**Δεν υπάρχει αποθηκευμένο πλήρες converted text για αυτή την πηγή. Δεν συμπληρώνεται αυθαίρετα.**\n")
    else:
        parts.append(f"\n**Λείπει το canonical source record `{source_path.relative_to(ROOT)}`. Δεν συμπληρώνεται αυθαίρετα.**\n")
    parts.append("\n## Β. Τι γράφτηκε στην πτυχιακή με βάση αυτή την πηγή\n")
    used = source_usage.get(sid, [])
    if not used:
        parts.append("\nΔεν εντοπίστηκε reader-visible block με αυτή την παραπομπή.\n")
    for row in used:
        ids = split_ids(row.get("source_ids") or "")
        other = [x for x in ids if x != sid]
        parts.append(f"\n### {row['id']}\n")
        parts.append(f"\n**Θέση:** {row.get('major','')} → {row.get('section','')}\n")
        if other:
            pretty = ", ".join(f"[{citation_map.get(x)}] `{x}`" for x in other)
            parts.append(f"\n**Η ίδια παράγραφος χρησιμοποιεί επίσης:** {pretty}\n")
        parts.append("\n**Κείμενο που υπάρχει τώρα στην πτυχιακή:**\n\n")
        parts.append((row.get("text") or "").strip() + "\n")
        parts.append(blank_editor())

parts.append("\n# Η τρέχουσα Βιβλιογραφία του Word\n")
for number in sorted(bib_entry):
    parts.append(f"\n[{number}] {bib_entry[number]}\n")
(out / "01_PIGES_KAI_KEIMENO_APO_PIGES.md").write_text("\n".join(parts), encoding="utf-8")


def render_selection(title: str, subtitle: str, selected: list[dict[str, str]]) -> str:
    result = [f"# {title}\n", subtitle + "\n"]
    last_major = None
    last_section = None
    for row in selected:
        if is_generated_list_cache(row) or row.get("major") == "Βιβλιογραφία" or is_heading(row):
            continue
        major = row.get("major") or ""
        section = row.get("section") or major
        if major != last_major:
            result.append(f"\n# {major}\n")
            last_major = major
            last_section = None
        if section != last_section:
            result.append(f"\n## {section}\n")
            last_section = section
        result.append(block(row))
    return "\n".join(result)


# 02 — Introduction/background synthesis without a citation in the same block, plus
# administrative/glossary text the student may want to review in the same pass.
theory_rows = []
for row in rows:
    major = row.get("major") or ""
    section = row.get("section") or ""
    ids = split_ids(row.get("source_ids") or "")
    include = (
        major in {
            "Κεφάλαιο 1 — Εισαγωγή",
            "Κεφάλαιο 2 — Θεωρητικό Υπόβαθρο και Σχετική Βιβλιογραφία",
        }
        and not ids
    )
    if major == "Front matter" and section in {
        "Δηλώσεις πνευματικών δικαιωμάτων και λογοκλοπής",
        "Γλωσσάριο και Ακρωνύμια", "Ακρωνύμια", "Βασικοί όροι",
    }:
        include = True
    if include:
        theory_rows.append(row)
(out / "02_THEORIA_KAI_SYNTHESI_XORIS_AMESI_PIGI.md").write_text(
    render_selection(
        "02 — Θεωρία / εισαγωγική σύνθεση χωρίς άμεση πηγή στο ίδιο κομμάτι",
        "Εδώ είναι τα θεωρητικά/εισαγωγικά κομμάτια που γράφτηκαν ως σύνθεση και **δεν έχουν άμεση εξωτερική παραπομπή στο συγκεκριμένο block**. Αυτό δεν σημαίνει ότι αποτελούν νέα επιστημονική πηγή· είναι κείμενο σύνδεσης, επεξήγησης, scope ή ορισμών που πρέπει να ελέγξεις και να γράψεις όπως το καταλαβαίνεις εσύ. Τα source-backed κομμάτια των Κεφαλαίων 1–2 βρίσκονται στο αρχείο 01 μαζί με τις πλήρεις πηγές τους.",
        theory_rows,
    ),
    encoding="utf-8",
)


# 03 — Entire methodology/implementation plus methodology/provenance/reproducibility appendices.
method_rows = []
for row in rows:
    major = row.get("major") or ""
    section = row.get("section") or ""
    include = major in {
        "Κεφάλαιο 3 — Μεθοδολογία και Πειραματικός Σχεδιασμός",
        "Κεφάλαιο 4 — Αρχιτεκτονική και Υλοποίηση του Συστήματος",
    }
    if major == "Παραρτήματα" and (
        section.startswith("Παράρτημα Α") or section.startswith("Α.")
        or section.startswith("Παράρτημα Γ") or section.startswith("Γ.")
        or section.startswith("Παράρτημα Δ") or section.startswith("Δ.")
    ):
        include = True
    if include:
        method_rows.append(row)
(out / "03_METHODOLOGIA_GRIDWORLD_KAI_EFARMOGI.md").write_text(
    render_selection(
        "03 — Μεθοδολογία, GridWorld και εφαρμογή",
        "Εδώ βρίσκεται ολόκληρο το reader-visible κείμενο της Μεθοδολογίας και της Υλοποίησης, μαζί με τα σχετικά παραρτήματα. Τα στοιχεία αυτά προέρχονται κυρίως από το δικό μας frozen protocol, το πραγματικό GridWorld/backend/application και τα provenance/reproducibility records. Όπου υπάρχει εξωτερική παραπομπή, εμφανίζεται δίπλα και το ίδιο κομμάτι υπάρχει επίσης στο αρχείο 01 μαζί με την πηγή.",
        method_rows,
    ),
    encoding="utf-8",
)


# 04 — Summary/Abstract + results/discussion/conclusions + result appendix.
result_rows = []
for row in rows:
    major = row.get("major") or ""
    section = row.get("section") or ""
    include = major in {
        "Κεφάλαιο 5 — Πειραματικά Αποτελέσματα",
        "Κεφάλαιο 6 — Συζήτηση",
        "Κεφάλαιο 7 — Συμπεράσματα και Μελλοντική Εργασία",
    }
    if major == "Front matter" and section in {"Περίληψη", "Abstract"}:
        include = True
    if major == "Παραρτήματα" and (
        section.startswith("Παράρτημα Β") or section.startswith("Β.")
    ):
        include = True
    if include:
        result_rows.append(row)
(out / "04_APOTELESMATA_SYZITISI_KAI_SYMPERASMATA.md").write_text(
    render_selection(
        "04 — Αποτελέσματα, ανάλυση, συζήτηση και συμπεράσματα",
        "Εδώ είναι η Περίληψη/Abstract, τα Κεφάλαια 5–7 και το Παράρτημα Β. Οι **αριθμητικές τιμές και τα frozen αποτελέσματα δεν πρέπει να αλλάξουν κατά την επαναδιατύπωση**. Μπορείς να αλλάξεις το πώς τα εξηγείς, αλλά όχι να δημιουργήσεις νέο αποτέλεσμα, να αλλάξεις denominator/interval/recovery status ή να ενισχύσεις ένα συμπέρασμα πέρα από όσα δείχνουν τα δεδομένα.",
        result_rows,
    ),
    encoding="utf-8",
)

files = sorted(out.glob("*.md"))
if len(files) != 4:
    raise RuntimeError(f"expected exactly four workbook files, got {files}")

missing_sources = [sid for sid in citation_map if not (SOURCES / f"{sid}.md").exists()]
empty_sources = [
    sid for sid in citation_map
    if (SOURCES / f"{sid}.md").exists()
    and not (SOURCES / f"{sid}.md").read_text(encoding="utf-8", errors="replace").strip()
]
manifest = {
    "file_count": 4,
    "formal_source_count": len(citation_map),
    "source_records_missing": missing_sources,
    "source_records_empty": empty_sources,
    "ledger_block_count": len(rows),
    "source_backed_block_occurrences": sum(len(v) for v in source_usage.values()),
}
print(json.dumps(manifest, ensure_ascii=False))
if missing_sources:
    raise RuntimeError(f"missing canonical full source records: {missing_sources}")
