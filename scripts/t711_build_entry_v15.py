#!/usr/bin/env python3
"""T-711A source-synchronized final hardening adapter.

The canonical Chapter 5 manuscript now contains the reviewed neutral result wording.
This adapter advances the source-drift pin to that exact reviewed source while keeping
the accepted synthesis graphic values and all frozen scientific assets unchanged.
"""

from __future__ import annotations

import json
from pathlib import Path

import t711_build_entry_v10 as v10
import t711_build_entry_v14 as v14


# Exact SHA-256 of the reviewed canonical CHAPTER_05_RESULTS.md after the T-711A
# source-level wording/terminology synchronization. Updating this pin requires a new
# deliberate review; it is not relaxed or removed.
EXPECTED_CANONICAL_CHAPTER_5_SHA256 = (
    "ba0dea0f8d46e3369dc22a3b18ca806b7ccbbe909e1592a3f21c193a703f2699"
)
v10.EXPECTED_CHAPTER_5_SHA256 = EXPECTED_CANONICAL_CHAPTER_5_SHA256

# Two v14 neutralizations are now already present in canonical Markdown. Register the
# canonical forms as idempotent source-synchronized transformations so v14's audit can
# still account for all three reviewed wording findings (the third remains in Ch. 6).
RQ1_SYNTHESIS_CANONICAL = (
    "Στο RQ1, Q-Learning, SARSA και Dyna-Q+ κατέληξαν στην ίδια τελική ονομαστική "
    "επίδοση, ενώ η εκτιμώμενη time-average επίδοση της Dyna-Q+ ήταν υψηλότερη κατά "
    "μήκος του διαθέσιμου προϋπολογισμού αλληλεπιδράσεων. Η DQN και η PPO είχαν "
    "χαμηλότερη τελική και time-average επίδοση και μεγαλύτερη διακύμανση μεταξύ "
    "ανεξάρτητων επαναλήψεων στο συγκεκριμένο ελεγχόμενο περιβάλλον και budget."
)
CROSS_RQ_SYNTHESIS_CANONICAL = (
    "Η σύνθεση αυτή δεν δημιουργεί ενιαία κατάταξη. Η Dyna-Q+ είχε την υψηλότερη "
    "καταγεγραμμένη time-average ονομαστική επίδοση, ενώ οι Q-Learning και SARSA "
    "εμφάνισαν τις υψηλότερες αναλογίες σταθερής ανάκαμψης στις δύο μόνιμες συνθήκες "
    "ανααντιστοίχισης. Η online προσαρμογή μπορεί να είναι ωφέλιμη, ουδέτερη ή "
    "επιβαρυντική ανάλογα με τον μηχανισμό της διαταραχής. Αυτές οι διαφοροποιήσεις "
    "αποτελούν το αντικείμενο της ερμηνείας στο επόμενο κεφάλαιο."
)
v14.TEXT_REPLACEMENTS[RQ1_SYNTHESIS_CANONICAL] = RQ1_SYNTHESIS_CANONICAL
v14.TEXT_REPLACEMENTS[CROSS_RQ_SYNTHESIS_CANONICAL] = CROSS_RQ_SYNTHESIS_CANONICAL


t711 = v14.t711
_previous_build = v14._build


def _build(output: Path, qa_output: Path) -> None:
    _previous_build(output, qa_output)
    report = json.loads(qa_output.read_text(encoding="utf-8"))
    report.update(
        {
            "t711a_hardening_version": 15,
            "canonical_results_source_synchronized": True,
            "canonical_results_source_sha256": EXPECTED_CANONICAL_CHAPTER_5_SHA256,
        }
    )
    qa_output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


t711.builder.build = _build

if __name__ == "__main__":
    t711.builder.main()
