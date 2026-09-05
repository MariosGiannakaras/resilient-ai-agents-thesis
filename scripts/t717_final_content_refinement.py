#!/usr/bin/env python3
"""Rebuild and validate the bounded T-717 thesis refinement from accepted T-716.

Scientific boundary: no experiment execution/re-analysis; protocol/results/T-612/T-613
quantitative assets are immutable; only document.xml and two explanatory media change.
"""
from __future__ import annotations
import argparse, base64, hashlib, json, re, zipfile, zlib
from pathlib import Path
from lxml import etree

ROOT=Path(__file__).resolve().parents[1]
DEFAULT_BASE=ROOT/"thesis/archive/T716_stage4_evidence_audited_review_ready.docx"
DEFAULT_OUT=ROOT/"thesis/archive/T717_pre_freeze_content_refined_review_ready.docx"
DEFAULT_QA=ROOT/"thesis/archive/T717_pre_freeze_content_refined_qa.json"
W="http://schemas.openxmlformats.org/wordprocessingml/2006/main"; NS={"w":W}
_SNIPPETS_B64 = Path(__file__).with_name("t717_snippets.b64").read_text(encoding="ascii").strip()
SNIPPETS=json.loads(zlib.decompress(base64.b64decode(_SNIPPETS_B64)).decode("utf-8"))
OLD_FIG1_CAPTION="Σχήμα 1 — Ροή του πειραματικού πρωτοκόλλου· τα ακριβή checkpoints προηγούνται των αντιστοιχισμένων κλάδων FN/FD/AN/AD."
OLD_FIG2_CAPTION="Σχήμα 2 — Αντιστοίχιση κάθε ερευνητικού ερωτήματος στα προκαθορισμένα μεγέθη εκτίμησης και στα καταγεγραμμένα αποτελέσματα."
HEADING_37="3.7 RQ1: μεγέθη εκτίμησης ονομαστικής μάθησης"
HEADING_612="6.12 Εγκυρότητα αναπαραγωγιμότητας"
AI_HEADING="2.1 Πράκτορες και διαδοχική λήψη αποφάσεων"
FIG2_NEXT="Η επιλογή αυτή αυξάνει το implementation overhead σε σχέση με ένα απλό script που εκπαιδεύει μοντέλα και τυπώνει μέσους όρους."
FUTURE_PREFIX="Η παρούσα μελέτη χρησιμοποιεί 32-interaction windows και fixed horizon 256."
BIB31_PREFIX="[31] Timofey Tomashevskiy"
EXPECTED_PLACEHOLDERS=["Ονοματεπώνυμο φοιτητή: [να συμπληρωθεί από το επίσημο έντυπο]","Student: [to be completed from the official form]","[Θέση για την ακριβή επίσημη δήλωση πριν από την τελική υποβολή]"]

def sha256(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def ptext(p):return "".join(p.xpath(".//w:t/text()",namespaces=NS))
def paragraphs(body):return [x for x in body if x.tag==f"{{{W}}}p"]
def find_unique(body,*,exact=None,prefix=None):
    hits=[]
    for p in paragraphs(body):
        t=ptext(p)
        if exact is not None and t==exact:hits.append(p)
        elif prefix is not None and t.startswith(prefix):hits.append(p)
    if len(hits)!=1:raise RuntimeError(f"expected one paragraph exact={exact!r} prefix={prefix!r}, found {len(hits)}")
    return hits[0]
def parse_snippet(name):return etree.fromstring(SNIPPETS[name].encode("utf-8"))
def insert_before(anchor,*nodes):
    parent=anchor.getparent(); idx=parent.index(anchor)
    for node in nodes:parent.insert(idx,node);idx+=1
def insert_after(anchor,*nodes):
    parent=anchor.getparent(); idx=parent.index(anchor)+1
    for node in nodes:parent.insert(idx,node);idx+=1
def remove_old_figure(body,caption_text):
    caption=find_unique(body,exact=caption_text); parent=caption.getparent(); idx=parent.index(caption)
    if idx==0:raise RuntimeError("caption has no preceding drawing paragraph")
    drawing=parent[idx-1]
    if not drawing.xpath(".//w:drawing",namespaces=NS):raise RuntimeError("preceding paragraph is not a drawing")
    parent.remove(drawing);parent.remove(caption)
def patch_document_xml(xml_bytes):
    root=etree.fromstring(xml_bytes,etree.XMLParser(remove_blank_text=False)); body=root.find(f".//{{{W}}}body")
    if body is None:raise RuntimeError("missing w:body")
    lof=None
    for p in paragraphs(body):
        instr=" ".join(p.xpath(".//w:instrText/text()",namespaces=NS))
        if "TOC" in instr and '\\c "Σχήμα"' in instr:lof=p;break
    if lof is None:raise RuntimeError("native List-of-Figures TOC field not found")
    lof.getparent().replace(lof,parse_snippet("lof"))
    remove_old_figure(body,OLD_FIG1_CAPTION);remove_old_figure(body,OLD_FIG2_CAPTION)
    insert_after(find_unique(body,exact=AI_HEADING),parse_snippet("ai_bridge"))
    insert_before(find_unique(body,exact=HEADING_37),parse_snippet("severity"),parse_snippet("fig1_drawing"),parse_snippet("fig1_caption"))
    insert_before(find_unique(body,prefix=FIG2_NEXT),parse_snippet("fig2_lead"),parse_snippet("fig2_drawing"),parse_snippet("fig2_caption"))
    insert_before(find_unique(body,exact=HEADING_612),parse_snippet("lim1"),parse_snippet("lim2"))
    future=find_unique(body,prefix=FUTURE_PREFIX);future.getparent().replace(future,parse_snippet("future"))
    insert_after(find_unique(body,prefix=BIB31_PREFIX),parse_snippet("bib32"))
    return etree.tostring(root,xml_declaration=True,encoding="UTF-8",standalone="yes")

def generate_figures(out_dir):
    import matplotlib;matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch,Rectangle,FancyArrowPatch
    out_dir.mkdir(parents=True,exist_ok=True);f1=out_dir/"figure1_gridworld_disturbances.png";f2=out_dir/"figure2_authority_dataflow.png"
    fig=plt.figure(figsize=(9.845,8.141),dpi=220);fig.suptitle("Τελικό GridWorld και παγωμένοι μηχανισμοί διαταραχής",fontsize=18,y=.985)
    layouts=[("Held-out layout A · seed 57001\n7×7 · shortest path 12 · max_steps 48",[(0,5),(1,2),(1,4),(3,5),(4,0),(5,4),(6,0),(6,3),(6,4)]),("Held-out layout B · seed 57002\n7×7 · shortest path 12 · max_steps 48",[(0,5),(2,3),(2,4),(2,5),(3,0),(3,2),(3,5),(3,6),(4,6)])]
    for (title,obs),pos in zip(layouts,[(.09,.52,.30,.33),(.59,.52,.30,.33)]):
        ax=fig.add_axes(pos);ax.set_xlim(-.5,6.5);ax.set_ylim(-.5,6.5);ax.set_aspect("equal");ax.set_xticks(range(7));ax.set_yticks(range(7));ax.grid(True,linewidth=.5,alpha=.35)
        for x,y in obs:ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor="0.22",edgecolor="0.22"))
        for x,y,label in [(0,0,"S"),(6,6,"G")]:ax.add_patch(Rectangle((x-.5,y-.5),1,1,facecolor="0.88",edgecolor="0.55"));ax.text(x,y,label,ha="center",va="center",fontsize=14,fontweight="bold")
        ax.set_title(title,fontsize=11,pad=6);ax.set_xlabel("x");ax.set_ylabel("y",rotation=0,labelpad=8)
        for spine in ax.spines.values():spine.set_alpha(.35)
    cards=[("Swap right/down",["up → up","right → down","down → right","left → left"],"persistent · unannounced"),("Clockwise cycle",["up → right","right → down","down → left","left → up"],"persistent · unannounced"),("Action failure",["intended aₜ","p=.15 → no-op","true state unchanged","reward −0.1"],"executed action hidden"),("Observation corruption",["transition first","p=.05 → false observation","uniform valid support","reward/transition unchanged"],"true state excluded")]
    for x,(head,lines,foot) in zip([.012,.272,.532,.792],cards):
        ax=fig.add_axes((x,.14,.196,.22));ax.set_axis_off();ax.add_patch(FancyBboxPatch((.02,.02),.96,.96,boxstyle="round,pad=.015",linewidth=1,facecolor="white",edgecolor="0.25"));ax.text(.5,.85,head,ha="center",va="center",fontsize=10.2,fontweight="bold")
        for y,t in zip([.65,.50,.35,.20],lines):ax.text(.5,y,t,ha="center",va="center",fontsize=9.1)
        ax.text(.5,.07,foot,ha="center",va="center",fontsize=8.2,fontstyle="italic",color="0.35")
    fig.text(.5,.045,"Τα p=.15 και p=.05 είναι συγκεκριμένα frozen severity points του protocol-v2.1, όχι severity sweep.",ha="center",fontsize=9.5);fig.savefig(f1,dpi=220,bbox_inches="tight",facecolor="white");plt.close(fig)
    fig=plt.figure(figsize=(10.386,5.55),dpi=220);ax=fig.add_axes((0,0,1,1));ax.set_axis_off();ax.text(.5,.957,"Αρχιτεκτονική ροή και επίπεδα επιστημονικής αυθεντίας",ha="center",va="center",fontsize=15.5,fontweight="bold")
    for y,h,label in [(.77,.17,"Scientific definition"),(.53,.17,"Execution & evidence"),(.29,.17,"Analysis & assets"),(.05,.17,"Presentation")]:ax.add_patch(FancyBboxPatch((.02,y),.96,h,boxstyle="round,pad=.005",linewidth=1,edgecolor="0.70",facecolor="0.97"));ax.text(.037,y+h/2,label,ha="left",va="center",fontsize=10.8,fontweight="bold")
    def box(x,y,w,h,text,fontsize=9.4):ax.add_patch(Rectangle((x,y),w,h,facecolor="white",edgecolor="0.25",linewidth=1));ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fontsize)
    def arrow(x1,y1,x2,y2):ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=10,linewidth=1,color="0.3"))
    box(.235,.80,.35,.10,"Frozen protocol / configuration",9.4);box(.605,.80,.35,.10,"Immutable StudyRecipe",9.4);arrow(.585,.85,.605,.85)
    xs=[.235,.355,.475,.595,.715,.835];labels=["Deterministic plan","Phase A","Exact checkpoint","Matched Phase B","Validation","Frozen evidence"];fonts=[7.9,8.6,7.9,7.8,8.5,7.9]
    for x,t,fs in zip(xs,labels,fonts):box(x,.56,.105,.10,t,fs)
    for x in xs[:-1]:arrow(x+.105,.61,x+.12,.61)
    box(.235,.32,.35,.10,"Predeclared T-612 analysis",9.2);box(.605,.32,.35,.10,"Registered T-613 thesis assets",9.2);arrow(.585,.37,.605,.37);box(.235,.08,.35,.10,"PySide6 UI",9.4);box(.605,.08,.35,.10,"Thesis / Word",9.4);arrow(.585,.13,.605,.13)
    arrow(.975,.77,.975,.705);ax.text(.955,.735,"materializes",ha="right",va="center",fontsize=8.8);arrow(.975,.53,.975,.465);ax.text(.955,.495,"validated evidence only",ha="right",va="center",fontsize=8.8);arrow(.975,.29,.975,.225);ax.text(.955,.255,"read-only projection",ha="right",va="center",fontsize=8.8)
    ax.text(.5,.018,"Το UI και το Word δεν επαναϋπολογίζουν estimands, thresholds, root/layout reductions ή intervals.",ha="center",va="bottom",fontsize=9.7,fontweight="bold");fig.savefig(f2,dpi=220,bbox_inches="tight",facecolor="white");plt.close(fig);return f1,f2

def write_docx(base,out,fig1,fig2):
    if not base.is_file():raise FileNotFoundError(base)
    out.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(base,"r") as zin:infos=zin.infolist();payload={i.filename:zin.read(i.filename) for i in infos}
    req={"word/document.xml","word/media/image1.png","word/media/image2.png"}
    if not req.issubset(payload):raise RuntimeError("T-716 baseline package layout changed unexpectedly")
    payload["word/document.xml"]=patch_document_xml(payload["word/document.xml"]);payload["word/media/image1.png"]=fig1.read_bytes();payload["word/media/image2.png"]=fig2.read_bytes()
    with zipfile.ZipFile(out,"w") as zout:
        for info in infos:zout.writestr(info,payload[info.filename])
def visible_text(xml):
    root=etree.fromstring(xml);return "\n".join("".join(p.xpath(".//w:t/text()",namespaces=NS)) for p in root.xpath(".//w:p",namespaces=NS))
def validate(base,out):
    with zipfile.ZipFile(base) as zb,zipfile.ZipFile(out) as zo:
        bn=zb.namelist();on=zo.namelist()
        if bn!=on:raise RuntimeError("OOXML entry set/order changed")
        changed=[n for n in bn if zb.read(n)!=zo.read(n)];expected=["word/document.xml","word/media/image1.png","word/media/image2.png"]
        if changed!=expected:raise RuntimeError(f"unexpected OOXML changes: {changed}")
        xml=zo.read("word/document.xml");root=etree.fromstring(xml);text=visible_text(xml);instr=root.xpath(".//w:instrText/text()",namespaces=NS);seq=sum("SEQ " in x for x in instr);toc=sum("TOC " in x for x in instr);page=int(b"PAGE" in zo.read("word/footer1.xml"));comments=int("word/comments.xml" in on);ins=len(root.xpath(".//w:ins",namespaces=NS));dele=len(root.xpath(".//w:del",namespaces=NS));media=[n for n in on if n.startswith("word/media/")];unch=sum(n not in ("word/media/image1.png","word/media/image2.png") and zb.read(n)==zo.read(n) for n in media)
        if len(media)!=25 or unch!=23 or (seq,toc,page)!=(27,3,1) or comments or ins or dele:raise RuntimeError(f"structural invariant mismatch media={len(media)} unchanged={unch} fields={seq,toc,page} comments/ins/del={comments,ins,dele}")
        if "SRC-" in text:raise RuntimeError("unresolved SRC-* residue")
        for marker in EXPECTED_PLACEHOLDERS:
            if marker not in text:raise RuntimeError(f"missing deliberate placeholder: {marker}")
        refs={int(m.group(1)) for m in re.finditer(r"(?m)^\[(\d+)\]\s",text)}
        if refs!=set(range(1,33)):raise RuntimeError(f"bibliography numbering mismatch: {sorted(refs)}")
        sent=["180 tuning units","q-c06","sarsa-c06","dqn-c05","ppo-c06","dyna-c03","0,15","0,05","256","32-interaction","0,10","(FN-FD)-(AN-AD)","right-censored"];missing=[s for s in sent if s not in text]
        if missing:raise RuntimeError(f"missing frozen sentinels: {missing}")
        return {"status":"pass","base":str(base),"output":str(out),"output_raw_sha256":sha256(out.read_bytes()),"changed_ooxml_entries":changed,"paragraph_count":len(root.xpath(".//w:body/w:p",namespaces=NS)),"reference_count":32,"references_used":"32/32","media_count":25,"unchanged_prior_media":23,"seq_fields":seq,"toc_fields":toc,"page_fields":page,"comments_xml":comments,"tracked_insertions":ins,"tracked_deletions":dele,"unresolved_src_residue":False,"placeholder_count":len(EXPECTED_PLACEHOLDERS),"scientific_results_modified":False,"new_experiment_or_reanalysis":False,"ui_screenshot_added":False,"ui_screenshot_disposition":"rejected historical development fixture; condition_unavailable/not-executed state is not representative scientific or implementation evidence"}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--base",type=Path,default=DEFAULT_BASE);ap.add_argument("--out",type=Path,default=DEFAULT_OUT);ap.add_argument("--qa",type=Path,default=DEFAULT_QA);ap.add_argument("--asset-dir",type=Path);a=ap.parse_args();assets=a.asset_dir or a.out.parent/"t717-generated-assets";f1,f2=generate_figures(assets);write_docx(a.base,a.out,f1,f2);qa=validate(a.base,a.out);qa["figure1_sha256"]=sha256(f1.read_bytes());qa["figure2_sha256"]=sha256(f2.read_bytes());a.qa.parent.mkdir(parents=True,exist_ok=True);a.qa.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(qa,ensure_ascii=False,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
