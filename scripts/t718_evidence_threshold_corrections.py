#!/usr/bin/env python3
"""Deterministic T-718 reader-facing corrections over canonical T-717.

No experiment, re-analysis, estimand, threshold, result, root/layout identity or
T-613 quantitative media may change. All 25 T-717 media remain present; only the
existing explanatory image1 is regenerated to rename Final layout A/B.
"""
from __future__ import annotations

import argparse, copy, hashlib, json, tempfile, zipfile
from pathlib import Path
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'thesis/archive/T717_pre_freeze_content_refined_review_ready.docx'
OUT=ROOT/'artifacts/t718/T718_evidence_threshold_corrected_review_ready.docx'
QA=ROOT/'artifacts/t718/T718_qa-report.json'
BASE_SHA='57d6de352eef6147fa24179f87a3f8e9ee39f65a90ad8b85777cac8f541f57c5'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}
XML_SPACE='{http://www.w3.org/XML/1998/namespace}space'


def file_sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def ptext(p): return ''.join(p.xpath('.//w:t/text()',namespaces=NS))
def paras(root): return root.xpath('.//w:body/w:p',namespaces=NS)


def keep_space(t):
    s=t.text or ''
    if s.startswith(' ') or s.endswith(' '): t.set(XML_SPACE,'preserve')
    elif XML_SPACE in t.attrib: del t.attrib[XML_SPACE]


def replace_exact_count(root,old:str,new:str,expected:int)->int:
    hits=[]
    for p in paras(root):
        nodes=p.xpath('.//w:t',namespaces=NS); joined=''.join(n.text or '' for n in nodes)
        start=0
        while True:
            idx=joined.find(old,start)
            if idx<0: break
            hits.append((nodes,idx,idx+len(old))); start=idx+len(old)
    if len(hits)!=expected: raise RuntimeError(f'expected {expected} Word-visible occurrence(s) of {old!r}; found {len(hits)}')
    if len({id(h[0]) for h in hits})!=len(hits): raise RuntimeError(f'multiple approved replacements in one paragraph for {old!r}')
    for nodes,start,end in hits:
        cursor=0; first=last=None; fo=lo=None
        for i,n in enumerate(nodes):
            s=n.text or ''; nxt=cursor+len(s)
            if first is None and start<nxt: first,fo=i,start-cursor
            if end<=nxt: last,lo=i,end-cursor; break
            cursor=nxt
        if first is None or last is None: raise RuntimeError(f'cannot map {old!r}')
        a,b=nodes[first],nodes[last]; prefix=(a.text or '')[:fo]; suffix=(b.text or '')[lo:]
        if first==last: a.text=prefix+new+suffix; keep_space(a)
        else:
            a.text=prefix+new; keep_space(a)
            for i in range(first+1,last): nodes[i].text=''; keep_space(nodes[i])
            b.text=suffix; keep_space(b)
    return expected


def find_one(root,*,exact=None,prefix=None):
    hits=[]
    for p in paras(root):
        s=ptext(p)
        if exact is not None and s==exact: hits.append(p)
        elif prefix is not None and s.startswith(prefix): hits.append(p)
    if len(hits)!=1: raise RuntimeError(f'expected one paragraph exact={exact!r} prefix={prefix!r}; found {len(hits)}')
    return hits[0]


def insert_after(anchor,text:str):
    p=etree.Element(f'{{{W}}}p'); ppr=anchor.find(f'{{{W}}}pPr')
    if ppr is not None: p.append(copy.deepcopy(ppr))
    r=etree.SubElement(p,f'{{{W}}}r'); t=etree.SubElement(r,f'{{{W}}}t'); t.text=text; keep_space(t)
    parent=anchor.getparent(); parent.insert(parent.index(anchor)+1,p)


def patch_xml(raw:bytes)->tuple[bytes,dict]:
    root=etree.fromstring(raw,etree.XMLParser(remove_blank_text=False)); c={}

    # C1 — define the already-frozen RQ2 scalar at its canonical methodology anchor.
    rq2=find_one(root,exact='Για κάθε method/root/layout/condition, η Phase B παρέχει τέσσερα matched outcomes FN, FD, AN και AD. Η απώλεια από τη διαταραχή υπό frozen deployment ορίζεται ως:')
    insert_after(rq2,
        'Κάθε FN/FD/AN/AD outcome χρησιμοποιεί το Phase-B return_sum, δηλαδή το μη προεξοφλημένο αθροιστικό task reward στις σταθερές 256 πραγματικές αλληλεπιδράσεις μετά το branch boundary. Το άθροισμα συνεχίζεται μεταξύ επεισοδίων και δεν επαναμηδενίζεται όταν το περιβάλλον κάνει episode reset.')
    c['C1_rq2_return_sum']=1

    # C2 — Frozen freezes learning state, not necessarily action stochasticity.
    replace_exact_count(root,'disturbance-associated loss υπό σταθερή πολιτική','disturbance-associated loss με παγωμένο το επιστημονικό learning state',1)
    fr=find_one(root,prefix='Οι όροι Frozen και Adaptive δεν δηλώνουν διαφορετικούς αλγορίθμους. Είναι δύο καθεστώτα deployment του ίδιου ακριβώς method checkpoint.')
    insert_after(fr,
        'Το Frozen δεν σημαίνει ντετερμινιστική επιλογή ενέργειας: οι ενημερώσεις του learning state είναι απενεργοποιημένες, αλλά η method-native στοχαστικότητα της behavior/inference διαδικασίας και το αντίστοιχο RNG state μπορούν να συνεχίσουν να εξελίσσονται. Αντίθετα, τα standardized Phase-A no-learning probes αποτελούν ξεχωριστή deterministic/greedy επιφάνεια τεκμηρίωσης.')
    c['C2_frozen_semantics']=1

    # C3 — only reader-facing references to the two actual final layouts.
    replace_exact_count(root,'δύο held-out διατάξεις','δύο τελικές διατάξεις',2)              # Summary + methodology
    replace_exact_count(root,'two held-out layouts','two final layouts reserved from development/tuning',1) # Abstract
    replace_exact_count(root,'των δύο held-out layouts','των δύο final layouts',1)           # Glossary
    replace_exact_count(root,'δύο held-out τελικές layouts','δύο τελικές layouts',1)          # Scope
    replace_exact_count(root,'δύο held-out layouts','δύο final layouts',2)                     # Results + external validity
    replace_exact_count(root,'Τα δύο τελικά held-out 7×7 layouts','Τα δύο τελικά 7×7 layouts',2) # LoF + caption
    main_layout=find_one(root,prefix='Η τελική εργασία χρησιμοποιεί δύο τελικές διατάξεις 7×7, τις gw-l1-final-a και gw-l1-final-b.')
    insert_after(main_layout,'Οι δύο final layouts κρατήθηκαν εκτός development/tuning μέχρι το άνοιγμα του final reserve και στη συνέχεια χρησιμοποιήθηκαν στην τελική πειραματική καμπάνια· δεν αποτελούν test-only unseen layouts.')
    c['C3_final_layout_terms']=10

    # C4 — bind the conclusion to the actual tested mechanism and RQ2 estimand.
    replace_exact_count(root,
        'αλλά μπορεί να μην προσφέρει όφελος ή ακόμη και να επιδεινώσει την επίδοση όταν το learning signal αλλοιώνεται από θόρυβο παρατήρησης.',
        'ενώ στο συγκεκριμένο observation-corruption-0.05 mechanism η Q-Learning και η SARSA παρουσίασαν αρνητικό adaptation benefit στο προδηλωμένο RQ2 estimand. Το αποτέλεσμα αυτό δεν γενικεύεται σε θόρυβο παρατήρησης ως κατηγορία.',1)
    c['C4_condition_scope']=1

    # C5 — explain the frozen ordinary Student-t CI without truncation/recomputation.
    ci=find_one(root,prefix='Η DQN είχε conditional recovery time 80,0 interactions, αλλά μόνο n=2 recovered roots και πολύ ευρύ interval [-529,9, 689,9].')
    insert_after(ci,
        'Το πολύ ευρύ Student-t interval με n=2 δεν είναι περιορισμένο από το φυσικό support 0–256 interactions· τα endpoints εκφράζουν sampling uncertainty της προκαθορισμένης ordinary Student-t summary και δεν αποτελούν φυσικά δυνατούς recovery times. Για αυτό η ερμηνεία παραμένει δεμένη με το recovered n και το right-censoring.')
    c['C5_ci_support_note']=1

    # C6 — exact immutable final execution identity; UI overlay explicitly separate.
    app=find_one(root,exact='Παράρτημα Δ — Αναπαραγωγή και λογισμικό περιβάλλον')
    insert_after(app,
        'Η accepted final scientific execution είναι η replacement Study protocol-v2.1-final--t610-recovery-01 από source commit 86fb01a13fd77b98ea0b8d8fa6d5c5d6e2cbd730, σε Windows 10.0.19045 και CPython 3.12.13, με clean tracked και non-output untracked source state όπως καταγράφεται στο final Study manifest. Η scientific recipe έχει SHA-256 8f21075ad2bc7a7944dbac4ba2ee2f3255ec0157706b94f99174b6d9ef99b154 και το deterministic plan SHA-256 073779d18f45caeab2ab725e7dce6b54b70394102d45de81e1974c7efaece0f4. Το locked scientific environment χρησιμοποιεί Gymnasium 1.3.0, Stable-Baselines3 2.9.0 και Torch 2.9.0. Η PySide6 6.11.2 είναι ξεχωριστό presentation/UI overlay και δεν αποτελεί μέρος της επιστημονικής execution identity.')
    c['C6_execution_identity']=1

    return etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes'),c


def make_image1(path:Path):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,Rectangle
    fig=plt.figure(figsize=(9.845,8.141),dpi=220); fig.suptitle('Τελικό GridWorld και παγωμένοι μηχανισμοί διαταραχής',fontsize=18,y=.985)
    layouts=[('Final layout A · seed 57001\n7×7 · shortest path 12 · max_steps 48',[(0,5),(1,2),(1,4),(3,5),(4,0),(5,4),(6,0),(6,3),(6,4)]),('Final layout B · seed 57002\n7×7 · shortest path 12 · max_steps 48',[(0,5),(2,3),(2,4),(2,5),(3,0),(3,2),(3,5),(3,6),(4,6)])]
    for (title,obs),pos in zip(layouts,[(.09,.52,.30,.33),(.59,.52,.30,.33)]):
        ax=fig.add_axes(pos); ax.set_xlim(-.5,6.5); ax.set_ylim(-.5,6.5); ax.set_aspect('equal'); ax.set_xticks(range(7)); ax.set_yticks(range(7)); ax.grid(True,linewidth=.5,alpha=.35)
        for x,y in obs: ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor='0.22',edgecolor='0.22'))
        for x,y,label in [(0,0,'S'),(6,6,'G')]: ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor='0.88',edgecolor='0.55')); ax.text(x,y,label,ha='center',va='center',fontsize=14,fontweight='bold')
        ax.set_title(title,fontsize=11,pad=6); ax.set_xlabel('x'); ax.set_ylabel('y',rotation=0,labelpad=8)
        for spine in ax.spines.values(): spine.set_alpha(.35)
    cards=[('Swap right/down',['up → up','right → down','down → right','left → left'],'persistent · unannounced'),('Clockwise cycle',['up → right','right → down','down → left','left → up'],'persistent · unannounced'),('Action failure',['intended aₜ','p=.15 → no-op','true state unchanged','reward −0.1'],'executed action hidden'),('Observation corruption',['transition first','p=.05 → false observation','uniform valid support','reward/transition unchanged'],'true state excluded')]
    for x,(head,lines,foot) in zip([.012,.272,.532,.792],cards):
        ax=fig.add_axes((x,.14,.196,.22)); ax.set_axis_off(); ax.add_patch(FancyBboxPatch((.02,.02),.96,.96,boxstyle='round,pad=.015',linewidth=1,facecolor='white',edgecolor='0.25')); ax.text(.5,.85,head,ha='center',va='center',fontsize=10.2,fontweight='bold')
        for y,t in zip([.65,.50,.35,.20],lines): ax.text(.5,y,t,ha='center',va='center',fontsize=9.1)
        ax.text(.5,.07,foot,ha='center',va='center',fontsize=8.2,fontstyle='italic',color='0.35')
    fig.text(.5,.045,'Τα p=.15 και p=.05 είναι συγκεκριμένα frozen severity points του protocol-v2.1, όχι severity sweep.',ha='center',fontsize=9.5)
    path.parent.mkdir(parents=True,exist_ok=True); fig.savefig(path,dpi=220,bbox_inches='tight',facecolor='white'); plt.close(fig)


def build(base:Path,out:Path,qa:Path)->dict:
    if file_sha(base)!=BASE_SHA: raise RuntimeError('canonical T-717 baseline SHA-256 mismatch')
    with zipfile.ZipFile(base) as z: infos=z.infolist(); payload={i.filename:z.read(i.filename) for i in infos}
    if not {'word/document.xml','word/media/image1.png','word/media/image2.png'}.issubset(payload): raise RuntimeError('unexpected T-717 OOXML layout')
    payload['word/document.xml'],changes=patch_xml(payload['word/document.xml'])
    with tempfile.TemporaryDirectory(prefix='t718-') as td:
        image1=Path(td)/'image1.png'; make_image1(image1); payload['word/media/image1.png']=image1.read_bytes(); out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(out,'w') as z:
            for info in infos: z.writestr(info,payload[info.filename])
    with zipfile.ZipFile(base) as a,zipfile.ZipFile(out) as b:
        if a.namelist()!=b.namelist(): raise RuntimeError('OOXML entry set/order changed')
        changed=[n for n in a.namelist() if a.read(n)!=b.read(n)]
        if changed!=['word/document.xml','word/media/image1.png']: raise RuntimeError(f'unexpected changed entries: {changed}')
        media=[n for n in b.namelist() if n.startswith('word/media/')]
        if len(media)!=25: raise RuntimeError(f'expected 25 media, found {len(media)}')
        if a.read('word/media/image2.png')!=b.read('word/media/image2.png'): raise RuntimeError('T-717 image2 changed')
        unchanged=sum(a.read(n)==b.read(n) for n in media)
    report={'status':'pass','base_raw_sha256':file_sha(base),'output_raw_sha256':file_sha(out),'changed_ooxml_entries':changed,'change_counts':changes,'media_count':25,'unchanged_media_count':unchanged,'image1_label_only_regeneration':True,'image2_preserved':True,'scientific_results_modified':False,'new_experiment_or_reanalysis':False,'protocol_or_estimand_modified':False,'visual_removed':False}
    qa.parent.mkdir(parents=True,exist_ok=True); qa.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); return report


def main():
    p=argparse.ArgumentParser(); p.add_argument('--base',type=Path,default=BASE); p.add_argument('--out',type=Path,default=OUT); p.add_argument('--qa',type=Path,default=QA); a=p.parse_args(); print(json.dumps(build(a.base,a.out,a.qa),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
