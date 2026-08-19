"""Conservative source-specific evidence adapter."""
from __future__ import annotations
import hashlib,re
from dataclasses import dataclass,asdict
from html.parser import HTMLParser
ALLOWED_GRADES=("ĐB","G1","G2","G3","G4","G5","G6","G7")
EXPECTED_COUNTS={"ĐB":1,"G1":1,"G2":2,"G3":6,"G4":4,"G5":6,"G6":3,"G7":4}
GRADE_ALIASES={"ĐẶC BIỆT":"ĐB","GIẢI ĐẶC BIỆT":"ĐB","GIẢI NHẤT":"G1","GIẢI NHÌ":"G2","GIẢI BA":"G3","GIẢI TƯ":"G4","GIẢI NĂM":"G5","GIẢI SÁU":"G6","GIẢI BẢY":"G7"}
NUMBER_RE=re.compile(r"^\d{2,5}$")
LEXICAL_RE=re.compile(r"GIẢI\s+ĐẶC\s+BIỆT|GIẢI\s+NHẤT|GIẢI\s+NHÌ|GIẢI\s+BA|GIẢI\s+TƯ|GIẢI\s+NĂM|GIẢI\s+SÁU|GIẢI\s+BẢY|ĐẶC\s+BIỆT|\d{2,5}",re.I)
@dataclass(frozen=True)
class SourceEvidenceCandidate:
    source_url:str; source_sha256:str; capture_timestamp_utc:str; grade_rows:dict[str,tuple[str,...]]; row_count:int; status:str; selector_diagnostics:dict[str,object]|None=None
    def as_dict(self): return asdict(self)
class _TableParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.tables=[]; self.text_tokens=[]; self._table=None; self._row=None; self._cell=None; self._skip_depth=0
    def handle_starttag(self,tag,attrs):
        tag=tag.lower()
        if tag in {"script","style","noscript","iframe"}: self._skip_depth+=1; return
        if self._skip_depth:return
        if tag=="table":self._table=[]
        elif tag=="tr" and self._table is not None:self._row=[]
        elif tag in {"td","th"} and self._row is not None:self._cell=[]
    def handle_endtag(self,tag):
        tag=tag.lower()
        if tag in {"script","style","noscript","iframe"}:self._skip_depth=max(0,self._skip_depth-1);return
        if self._skip_depth:return
        if tag in {"td","th"} and self._row is not None and self._cell is not None:self._row.append(" ".join("".join(self._cell).split()));self._cell=None
        elif tag=="tr" and self._table is not None and self._row is not None:
            if self._row:self._table.append(self._row)
            self._row=None
        elif tag=="table" and self._table is not None:
            if self._table:self.tables.append(self._table)
            self._table=None
    def handle_data(self,data):
        if self._skip_depth:return
        if self._cell is not None:self._cell.append(data)
        self.text_tokens.extend(m.upper() for m in LEXICAL_RE.findall(data))
def _canonical_grade(label):
    n=" ".join(label.upper().split());return n if n in ALLOWED_GRADES else GRADE_ALIASES.get(n)
def _validate_counts(rows):return all(len(rows.get(g,()))==n for g,n in EXPECTED_COUNTS.items())
def _candidate_from_table(table):
    rows={}
    for cells in table:
        if not cells:continue
        grade=_canonical_grade(cells[0])
        if grade is None:continue
        nums=tuple(n for cell in cells[1:] for n in re.findall(r"\d{2,5}",cell))
        if nums:rows[grade]=tuple(rows.get(grade,()))+nums
    return rows if _validate_counts(rows) else None
def _candidate_from_ordered_tokens(tokens):
    grade_hits=[(i,_canonical_grade(t)) for i,t in enumerate(tokens) if _canonical_grade(t) is not None]
    diagnostics={"grade_token_counts":{g:sum(1 for _,x in grade_hits if x==g) for g in ALLOWED_GRADES},"ordered_sequence_candidates":0,"recent_db_segment_counts":[]}
    for start,token in enumerate(tokens):
        if _canonical_grade(token)!="ĐB":continue
        diagnostics["ordered_sequence_candidates"]+=1;rows={};pos=start;valid=True;segments=[]
        for grade in ALLOWED_GRADES:
            if pos>=len(tokens) or _canonical_grade(tokens[pos])!=grade:valid=False;break
            pos+=1;nums=[]
            while pos<len(tokens) and _canonical_grade(tokens[pos]) is None:
                if NUMBER_RE.fullmatch(tokens[pos]):nums.append(tokens[pos])
                pos+=1
            segments.append(len(nums))
            if len(nums)!=EXPECTED_COUNTS[grade]:valid=False;break
            rows[grade]=tuple(nums)
        if start>=max(0,len(tokens)-500):diagnostics["recent_db_segment_counts"]=(diagnostics["recent_db_segment_counts"]+[segments])[-5:]
        if valid and _validate_counts(rows):return rows,diagnostics
    return None,diagnostics
def extract_xsmb_candidate(html,source_url,capture_timestamp_utc):
    p=_TableParser();p.feed(html);p.close();selected=None;diagnostics={}
    for table in p.tables:
        c=_candidate_from_table(table)
        if c is not None:selected=c;break
    if selected is None:selected,diagnostics=_candidate_from_ordered_tokens(p.text_tokens)
    sha=hashlib.sha256(html.encode("utf-8")).hexdigest()
    if selected is None:return SourceEvidenceCandidate(source_url,sha,capture_timestamp_utc,{},0,"NO_RESULT_TABLE_CANDIDATE",diagnostics)
    return SourceEvidenceCandidate(source_url,sha,capture_timestamp_utc,selected,sum(map(len,selected.values())),"CANDIDATE_ONLY",diagnostics)
