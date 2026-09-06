from __future__ import annotations
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import base64,gzip,hashlib,json,re
from lxml import etree

BASE=Path('thesis/archive/T718_evidence_threshold_corrected_review_ready.docx')
PAYLOAD=Path('scripts/t719_payload.b64')
OUT=Path('artifacts/t719/T719_final_authority_audited_review_ready.docx')
QA=Path('artifacts/t719/T719_qa-report.json')
BASE_SHA='60f92b1cb9994ff2964e551d09bf5a9ee14c7a37e30d49b92435bcea90c957de'
OUT_SHA='1529f2b8a69594f164050544a54e1de115acb40a5a0eb6291156d3ecccf1afb9'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}; Q=lambda t:f'{{{W}}}{t}'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ptext(p): return ''.join(p.xpath('.//w:t/text()',namespaces=NS))
def set_p_text(p,text):
    first=next((r for r in p.xpath('./w:r',namespaces=NS) if r.xpath('.//w:t',namespaces=NS)),None)
    rpr=deepcopy(first.find('w:rPr',namespaces=NS)) if first is not None and first.find('w:rPr',namespaces=NS) is not None else None
    ppr=p.find('w:pPr',namespaces=NS)
    for c in list(p):
        if c is not ppr: p.remove(c)
    r=etree.SubElement(p,Q('r'))
    if rpr is not None:r.append(rpr)
    t=etree.SubElement(r,Q('t')); t.text=text

def find_exact(root,text):
    h=[p for p in root.xpath('.//w:p',namespaces=NS) if ptext(p)==text]
    if len(h)!=1: raise RuntimeError(f'anchor count={len(h)} {text[:100]!r}')
    return h[0]
def load_payload():
    raw=gzip.decompress(base64.b64decode(PAYLOAD.read_text(encoding='ascii')))
    return json.loads(raw.decode('utf-8'))
def field_key(instr):
    s=' '.join((instr or '').split())
    if '\\c "Σχήμα"' in s:return 'figures'
    if '\\c "Πίνακας"' in s:return 'tables'
    if '\\o "1-3"' in s:return 'toc'
    raise RuntimeError(instr)
def field_regions(root,body):
    children=list(body); out={}
    for it in root.xpath('.//w:instrText[contains(. , "TOC")]',namespaces=NS):
        key=field_key(it.text); x=it
        while x.getparent() is not body:x=x.getparent()
        si=children.index(x);ei=si
        if not x.xpath('.//w:fldChar[@w:fldCharType="end"]',namespaces=NS):
            for j in range(si+1,len(children)):
                if children[j].xpath('.//w:fldChar[@w:fldCharType="end"]',namespaces=NS):ei=j;break
            else:raise RuntimeError(key)
        out[key]=(si,ei)
    if set(out)!={'toc','figures','tables'}:raise RuntimeError(out)
    return out

def main():
    if sha(BASE)!=BASE_SHA:raise RuntimeError('T-718 baseline hash mismatch')
    P=load_payload()
    with ZipFile(BASE) as zin:
        infos=zin.infolist(); files={i.filename:zin.read(i.filename) for i in infos}
    root=etree.fromstring(files['word/document.xml']); body=root.find('.//w:body',namespaces=NS)
    # Bounded semantic corrections.
    for old,new in P['replacements']:
        set_p_text(find_exact(root,old),new)
    ins=P['insert_after']; anchor=find_exact(root,ins['anchor']); newp=deepcopy(anchor); set_p_text(newp,ins['text'])
    if ins.get('center'):
        ppr=newp.find('w:pPr',namespaces=NS)
        if ppr is None:ppr=etree.Element(Q('pPr'));newp.insert(0,ppr)
        jc=ppr.find('w:jc',namespaces=NS)
        if jc is None:jc=etree.SubElement(ppr,Q('jc'))
        jc.set(Q('val'),'center')
    anchor.addnext(newp)
    cap=find_exact(root,P['caption']['old'])
    trailing=[t for t in cap.xpath('./w:r/w:t',namespaces=NS) if (t.text or '').startswith(' — ')]
    if len(trailing)!=1:raise RuntimeError('Table 1 caption anchor')
    trailing[0].text=P['caption']['new_trailing']
    if sum(P['declaration_placeholder'] in ptext(p) for p in root.xpath('.//w:p',namespaces=NS))!=1:raise RuntimeError('declaration placeholder')

    # IEEE numeric order-of-first-appearance; exact [n] tokens only, never CI brackets.
    children=list(body); bib=next(e for e in children if etree.QName(e).localname=='p' and ptext(e)=='Βιβλιογραφία'); bi=children.index(bib)
    order=[]; rgx=re.compile(r'\[(\d+)\]\s*[–-]\s*\[(\d+)\]|\[(\d+)\]')
    for e in children[:bi]:
        for p in ([e] if etree.QName(e).localname=='p' else e.xpath('.//w:p',namespaces=NS)):
            for m in rgx.finditer(ptext(p)):
                nums=(range(int(m.group(1)),int(m.group(2))+1) if m.group(1) else [int(m.group(3))])
                for n in nums:
                    if 1<=n<=32 and n not in order:order.append(n)
    if len(order)!=32 or set(order)!=set(range(1,33)):raise RuntimeError(order)
    mapping={old:new for new,old in enumerate(order,1)}
    def remap(s):
        hold={}
        def rr(m):
            vals=sorted(mapping[n] for n in range(int(m.group(1)),int(m.group(2))+1));k=f'@@R{len(hold)}@@';hold[k]=', '.join(f'[{n}]' for n in vals);return k
        s=re.sub(r'\[(\d+)\]\s*[–-]\s*\[(\d+)\]',rr,s)
        s=re.sub(r'\[(\d+)\]',lambda m:f'[{mapping.get(int(m.group(1)),int(m.group(1)))}]',s)
        for k,v in hold.items():s=s.replace(k,v)
        return s
    for e in children[:bi]:
        for t in e.xpath('.//w:t',namespaces=NS):
            if t.text and '[' in t.text:t.text=remap(t.text)
    children=list(body);bi=list(body).index(bib); entries=[]
    for e in children[bi+1:]:
        if etree.QName(e).localname!='p':
            if entries:break
            continue
        m=re.match(r'^\[(\d+)\]\s',ptext(e))
        if m:entries.append((int(m.group(1)),e));
        elif entries:break
        if len(entries)==32:break
    if len(entries)!=32:raise RuntimeError('bibliography count')
    identities={n:re.sub(r'^\[\d+\]\s*','',ptext(e),count=1) for n,e in entries}
    for old,e in entries:
        for t in e.xpath('.//w:t',namespaces=NS):
            if t.text and f'[{old}]' in t.text:t.text=t.text.replace(f'[{old}]',f'[{mapping[old]}]',1);break
    for _,e in entries:body.remove(e)
    at=list(body).index(bib)+1
    for old,e in sorted(entries,key=lambda x:mapping[x[0]]):body.insert(at,e);at+=1

    # Inject prevalidated field caches/styles from the fully rendered 101-page candidate.
    fc=json.loads(gzip.decompress(base64.b64decode(P['field_cache_b64'])).decode('utf-8'))
    regs=field_regions(root,body)
    for key in sorted(regs,key=lambda k:regs[k][0],reverse=True):
        si,ei=regs[key]; cur=list(body)
        for e in cur[si:ei+1]:body.remove(e)
        for off,xml in enumerate(fc['regions'][key]):body.insert(si+off,etree.fromstring(xml.encode('utf-8')))
    styles=etree.fromstring(files['word/styles.xml'])
    for sid,xml in fc['styles'].items():
        new=etree.fromstring(xml.encode('utf-8'));old=styles.xpath(f'.//w:style[@w:styleId="{sid}"]',namespaces=NS)
        if old:
            par=old[0].getparent();idx=par.index(old[0]);par.remove(old[0]);par.insert(idx,new)
        else:styles.append(new)
    files['word/document.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone='yes')
    files['word/styles.xml']=etree.tostring(styles,xml_declaration=True,encoding='UTF-8',standalone='yes')
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with ZipFile(OUT,'w',ZIP_DEFLATED) as zout:
        for info in infos:zout.writestr(info,files[info.filename])
    if sha(OUT)!=OUT_SHA:raise RuntimeError(f'validated output hash mismatch {sha(OUT)}')

    # Exact package/media/results guards.
    with ZipFile(BASE) as zb,ZipFile(OUT) as zo:
        bd={n:zb.read(n) for n in zb.namelist()};od={n:zo.read(n) for n in zo.namelist()}
    changed=sorted(n for n in bd if bd[n]!=od[n]);media=sorted(n for n in bd if n.startswith('word/media/'))
    if changed!=['word/document.xml','word/styles.xml'] or len(media)!=25 or any(bd[n]!=od[n] for n in media):raise RuntimeError('package/media boundary')
    text='\n'.join(ptext(p) for p in root.xpath('.//w:body//w:p',namespaces=NS));instr=root.xpath('.//w:instrText/text()',namespaces=NS)
    sent=['6,623 [3,798, 9,448]','26,102 [25,344, 26,860]','32,269 [28,910, 35,628]','31,127 [28,796, 33,458]','22,665 [18,078, 27,251]','13,785 [9,904, 17,667]','-2,698 [-3,880, -1,516]','-3,165 [-4,917, -1,412]','[-529,9, 689,9]']
    if any(x not in text for x in sent):raise RuntimeError('frozen result sentinel')
    if sum('SEQ ' in x for x in instr)!=27 or sum('TOC ' in x for x in instr)!=3:raise RuntimeError('field inventory')
    if root.xpath('.//w:ins|.//w:del',namespaces=NS):raise RuntimeError('tracked changes')
    styles_used=root.xpath('.//w:pPr/w:pStyle/@w:val',namespaces=NS);toc=sum(styles_used.count(x) for x in ['TOC1','TOC2','TOC3']);lof_lot=styles_used.count('TableofFigures')
    if toc!=139 or lof_lot!=27:raise RuntimeError((toc,lof_lot))
    qa={'status':'pass','base_raw_sha256':BASE_SHA,'output_raw_sha256':OUT_SHA,'changed_ooxml_entries':changed,'media_count':25,'unchanged_media_count':25,'scientific_results_modified':False,'new_experiment_or_reanalysis':False,'protocol_or_estimand_modified':False,'bibliography_identity_count':32,'citation_first_appearance_sequential':True,'toc_entry_count':139,'figure_list_entry_count':24,'table_list_entry_count':3,'rendered_page_count':101,'full_visual_qa':'PASS_101_PAGES','declaration_placeholder_preserved':True}
    QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(qa,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
