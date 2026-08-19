"""Conservative source-specific evidence adapter.

This adapter belongs to the DATA admission boundary. It may extract a candidate
XSMB result table from an already-captured HTML document, but it has NO authority
to declare canonical truth, quorum, signal, prediction, or risk.

Design rules:
- selector allowlist only;
- advertisement/navigation/free-text regions are never accepted as result rows;
- only one bounded result candidate is emitted per capture;
- raw HTML is not retained in the returned object;
- numeric payload is represented compactly and can be hashed by the caller;
- no bulk history is loaded into memory.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, asdict
from html.parser import HTMLParser

ALLOWED_GRADES = ("ĐB", "G1", "G2", "G3", "G4", "G5", "G6", "G7")
EXPECTED_COUNTS = {"ĐB": 1, "G1": 1, "G2": 2, "G3": 6, "G4": 4, "G5": 6, "G6": 3, "G7": 4}
GRADE_ALIASES = {
    "ĐẶC BIỆT": "ĐB",
    "GIẢI ĐẶC BIỆT": "ĐB",
    "GIẢI NHẤT": "G1",
    "GIẢI NHÌ": "G2",
    "GIẢI BA": "G3",
    "GIẢI TƯ": "G4",
    "GIẢI NĂM": "G5",
    "GIẢI SÁU": "G6",
    "GIẢI BẢY": "G7",
}
NUMBER_RE = re.compile(r"^\d{2,5}$")


@dataclass(frozen=True)
class SourceEvidenceCandidate:
    source_url: str
    source_sha256: str
    capture_timestamp_utc: str
    grade_rows: dict[str, tuple[str, ...]]
    row_count: int
    status: str

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class _TableParser(HTMLParser):
    """Collect bounded text evidence while ignoring executable/embedded content."""

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
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        if tag in {"script", "style", "noscript", "iframe"}:
            self._skip_depth = max(0, self._skip_depth - 1)
            return
        if self._skip_depth:
            return
        if tag in {"td", "th"} and self._row is not None and self._cell is not None:
            text = " ".join("".join(self._cell).split())
            self._row.append(text)
            self._cell = None
        elif tag == "tr" and self._table is not None and self._row is not None:
            if self._row:
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            if self._table:
                self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str):
        if self._skip_depth:
            return
        text = " ".join(data.split())
        if not text:
            return
        # Keep a bounded lexical stream for the fallback selector. This is not
        # source classification: it is only used to detect the exact ordered
        # XSMB grade grammar below.
        self.text_tokens.append(text)
        if self._cell is not None:
            self._cell.append(data)


def _canonical_grade(label: str) -> str | None:
    normalized = " ".join(label.upper().split())
    if normalized in ALLOWED_GRADES:
        return normalized
    return GRADE_ALIASES.get(normalized)


def _validate_counts(rows: dict[str, tuple[str, ...]]) -> bool:
    return all(len(rows.get(grade, ())) == count for grade, count in EXPECTED_COUNTS.items())


def _candidate_from_table(table: list[list[str]]) -> dict[str, tuple[str, ...]] | None:
    rows: dict[str, tuple[str, ...]] = {}
    for cells in table:
        if not cells:
            continue
        grade = _canonical_grade(cells[0])
        if grade is None:
            continue
        numbers = tuple(cell for cell in cells[1:] if NUMBER_RE.fullmatch(cell))
        if not numbers:
            continue
        rows.setdefault(grade, numbers)
    if _validate_counts(rows):
        return rows
    return None


def _candidate_from_ordered_tokens(tokens: list[str]) -> dict[str, tuple[str, ...]] | None:
    """Fallback for modern markup where result cells are not enclosed in tables.

    Admission requires one contiguous ordered grade sequence and exact XSMB
    cardinalities. This remains candidate-only and cannot grant canonicality.
    """
    for start, token in enumerate(tokens):
        if _canonical_grade(token) != "ĐB":
            continue
        rows: dict[str, tuple[str, ...]] = {}
        pos = start
        valid = True
        for grade in ALLOWED_GRADES:
            if pos >= len(tokens) or _canonical_grade(tokens[pos]) != grade:
                valid = False
                break
            pos += 1
            nums: list[str] = []
            while pos < len(tokens) and _canonical_grade(tokens[pos]) is None:
                if NUMBER_RE.fullmatch(tokens[pos]):
                    nums.append(tokens[pos])
                pos += 1
                if len(nums) > EXPECTED_COUNTS[grade]:
                    valid = False
                    break
            if not valid or len(nums) != EXPECTED_COUNTS[grade]:
                valid = False
                break
            rows[grade] = tuple(nums)
        if valid and _validate_counts(rows):
            return rows
    return None


def extract_xsmb_candidate(html: str, source_url: str, capture_timestamp_utc: str) -> SourceEvidenceCandidate:
    """Extract one candidate XSMB table; never declare it canonical."""
    parser = _TableParser()
    parser.feed(html)
    parser.close()

    selected: dict[str, tuple[str, ...]] | None = None
    for table in parser.tables:
        candidate = _candidate_from_table(table)
        if candidate is not None:
            selected = candidate
            break
    if selected is None:
        selected = _candidate_from_ordered_tokens(parser.text_tokens)

    source_sha256 = hashlib.sha256(html.encode("utf-8")).hexdigest()
    if selected is None:
        return SourceEvidenceCandidate(
            source_url=source_url,
            source_sha256=source_sha256,
            capture_timestamp_utc=capture_timestamp_utc,
            grade_rows={},
            row_count=0,
            status="NO_RESULT_TABLE_CANDIDATE",
        )

    return SourceEvidenceCandidate(
        source_url=source_url,
        source_sha256=source_sha256,
        capture_timestamp_utc=capture_timestamp_utc,
        grade_rows=selected,
        row_count=sum(len(values) for values in selected.values()),
        status="CANDIDATE_ONLY",
    )
