#!/usr/bin/env python3
"""Read-only diagnostics for exact Word-visible T-717 anchors."""
from pathlib import Path
import zipfile
from lxml import etree

DOC=Path('thesis/archive/T717_pre_freeze_content_refined_review_ready.docx')
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}
with zipfile.ZipFile(DOC) as z:
    root=etree.fromstring(z.read('word/document.xml'))
ps=[''.join(p.xpath('.//w:t/text()',namespaces=NS)) for p in root.xpath('.//w:body/w:p',namespaces=NS)]
needles=['RQ2','return_sum','Frozen','held-out','gw-l1-final','conditional recovery time','80,0 interactions','Παράρτημα Ε','θόρυβο παρατήρησης']
for i,s in enumerate(ps):
    if any(n.lower() in s.lower() for n in needles):
        print(f'P{i}: {s}')
