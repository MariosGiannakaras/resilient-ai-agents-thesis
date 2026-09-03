#!/usr/bin/env python3
# One-shot exact replacement; this touch triggers the temporary workflow.
from pathlib import Path

path = Path("docs/thesis/draft/CHAPTER_02_BACKGROUND_RELATED_WORK.md")
text = path.read_text(encoding="utf-8")
old = "Έτσι, τα αποτελέσματα λειτουργούν ως ελεγχόμενο σημείο αναφοράς για τη μελέτη ανθεκτικότητας και προσαρμογής και όχι ως καθολική κατάταξη σύγχρονων τεχνικών continual RL. Οι ερμηνείες περιορίζονται στους συγκεκριμένους μηχανισμούς και στο παρόν πειραματικό πρωτόκολλο."
new = "Έτσι, τα αποτελέσματα αποτελούν ελεγχόμενο σημείο αναφοράς για την ανθεκτικότητα και την προσαρμογή, όχι καθολική κατάταξη τεχνικών continual RL. Οι ερμηνείες περιορίζονται στο παρόν πειραματικό πρωτόκολλο."
if text.count(old) != 1:
    raise RuntimeError(f"Expected exactly one current Chapter 2 closing paragraph, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
