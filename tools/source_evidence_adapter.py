"""Conservative source-specific evidence adapter."""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, asdict
from html.parser import HTMLParser

ALLOWED_GRADES = ("ĐB", "G1", "G2", "G3", "G4", "G5", "G6", "G7")
EXPECTED_COUNTS = {"ĐB": 1, "G1": 1, "G2": 2, "G3": 6, "G4": 4, "G5": 6, "G6": 3, "G7": 4}
GRADE_ALIASES = {
    "ĐẶC BIỆT": "ĐB", "GIẢI ĐẶC BIỆT": "ĐB", "GIẢI NHẤT": "G1",
    "GIẢI NHÌ": "G2", "GIẢI BA": "G3", "GIẢI TƯ": "G4",
    "GIẢI NĂM": "G5", "GIẢI SÁU": "G6", "GIẢI BẢY": "G7",
}
NUMBER_RE = re.compile(r"^\d{2,5}$")
LEXICAL_RE = re.compile(
    r"GIẢI\s+ĐẶC\s+BIỆT|GIẢI\s+NHẤT|GIẢI\s+NHÌ|GIẢI\s+BA|GIẢI\s+TƯ|GIẢI\s+NĂM|GIẢI\s+SÁU|GIẢI\s+BẢY|ĐẶC\s+BIỆT|\d{2,5}",
    re.I,
)


@dataclass(frozen=True)
class SourceEvidenceCandidate:
    source_url: str
    source_sha256: str
    capture_timestamp_utc: str
    grade_rows: dict[str, tuple[str, ...]]
    row_count: int
    status: str
    selector_diagnostics: dict[str, object] | None = None

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tables: list[list[list[str]]] = []
        self.text_tokens: list[str] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs):
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "iframe"}:
            self._skip_depth += 1; return
        if self._skip_depth: return
        if tag == "table": self._table = []
        elif tag == "tr" and self._table is not None: self._row = []
        elif tag in {"td", "th"} and self._row is not None: self._cell = []

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "iframe"}:
            self._skip_depth = max(0, self._skip_depth - 1); return
        if self._skip_depth: return
        if tag in {"td", "th"} and self._row is not None and self._cell is not None:
            self._row.append(" ".join("".join(self._cell).split())); self._cell = None
        elif tag == "tr" and self._table is not None and self._row is not None:
            if self._row: self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            if self._table: self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str):
        if self._skip_depth: return
        if self._cell is not None: self._cell.append(data)
        self.text_tokens.extend(match.upper() for match in LEXICAL_RE.findall(data))


def _canonical_grade(label: str) -> str | None:
    normalized = " ".join(label.upper().split())
    if normalized in ALLOWED_GRADES: return normalized
    return GRADE_ALIASES.get(normalized)


def _validate_counts(rows: dict[str, tuple[str, ...]]) -> bool:
    return all(len(rows.get(grade, ())) == count for grade, count in EXPECTED_COUNTS.items())


def _candidate_from_table(table: list[list[str]]) -> dict[str, tuple[str, ...]] | None:
    rows: dict[str, tuple[str, ...]] = {}
    for cells in table:
        if not cells: continue
        grade = _canonical_grade(cells[0])
        if grade is None: continue
        numbers = tuple(n for cell in cells[1:] for n in re.findall(r"\d{2,5}", cell))
        if not numbers: continue
        rows.setdefault(grade, numbers)
    return rows if _validate_counts(rows) else None


def _candidate_from_ordered_tokens(tokens: list[str]) -> tuple[dict[str, tuple[str, ...]] | None, dict[str, object]]:
    grade_hits = [(i, _canonical_grade(t)) for i, t in enumerate(tokens)]
    grade_hits = [(i, g) for i, g in grade_hits if g is not None]
    diagnostics = {
        "grade_token_counts": {grade: sum(1 for _, g in grade_hits if g == grade) for grade in ALLOWED_GRADES},
        "ordered_sequence_candidates": 0,
    }
    for start, token in enumerate(tokens):
        if _canonical_grade(token) != "ĐB": continue
        diagnostics["ordered_sequence_candidates"] += 1
        rows: dict[str, tuple[str, ...]] = {}
        pos = start
        valid = True
        for grade in ALLOWED_GRADES:
            if pos >= len(tokens) or _canonical_grade(tokens[pos]) != grade:
                valid = False; break
            pos += 1
            nums: list[str] = []
            while pos < len(tokens) and _canonical_grade(tokens[pos]) is None:
                if NUMBER_RE.fullmatch(tokens[pos]): nums.append(tokens[pos])
                pos += 1
                if len(nums) > EXPECTED_COUNTS[grade]: valid = False; break
            if not valid or len(nums) != EXPECTED_COUNTS[grade]: valid = False; break
            rows[grade] = tuple(nums)
        if valid and _validate_counts(rows): return rows, diagnostics
    return None, diagnostics


def extract_xsmb_candidate(html: str, source_url: str, capture_timestamp_utc: str) -> SourceEvidenceCandidate:
    parser = _TableParser(); parser.feed(html); parser.close()
    selected = None; diagnostics: dict[str, object] = {}
    for table in parser.tables:
        candidate = _candidate_from_table(table)
        if candidate is not None: selected = candidate; break
    if selected is None: selected, diagnostics = _candidate_from_ordered_tokens(parser.text_tokens)
    source_sha256 = hashlib.sha256(html.encode("utf-8")).hexdigest()
    if selected is None:
        return SourceEvidenceCandidate(source_url, source_sha256, capture_timestamp_utc, {}, 0, "NO_RESULT_TABLE_CANDIDATE", diagnostics)
    return SourceEvidenceCandidate(source_url, source_sha256, capture_timestamp_utc, selected, sum(map(len, selected.values())), "CANDIDATE_ONLY", diagnostics)
