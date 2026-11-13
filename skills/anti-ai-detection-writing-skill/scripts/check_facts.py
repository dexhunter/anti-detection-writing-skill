#!/usr/bin/env python3
"""Compare numbers, dates, prices, order IDs, and capitalised names.

The source is the fact-complete text. The candidate is the text about to be
scanned. A difference means a fact is missing, changed, or added. This does
not judge prose, authorship, or a detector score. Numeric dates are read
day-first, as in UK correspondence. A range such as "1–2 November" is both
days; with no year the stored year is 0000. A single capitalised word at the
start of a sentence is not treated as a name.
"""

import argparse
import itertools
import json
import re
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

LIMIT = (
    "Compares extracted numbers, dates, prices, order IDs, and capitalised "
    "names. A day range such as 1–2 November is both days. A single "
    "capitalised word at the start of a sentence is not treated as a name. "
    "It does not judge prose, authorship, or a detector score."
)

MONTHS = {
    "jan": 1, "january": 1, "feb": 2, "february": 2, "mar": 3, "march": 3,
    "apr": 4, "april": 4, "may": 5, "jun": 6, "june": 6, "jul": 7, "july": 7,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "oct": 10,
    "october": 10, "nov": 11, "november": 11, "dec": 12, "december": 12,
}

PRICE_RE = re.compile(
    r"(?:(?<![A-Za-z])(?P<word>GBP|USD|EUR)|(?P<symbol>[£$€]))"
    r"\s?(?P<amount>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)"
)
WRITTEN_DATE_RE = re.compile(
    r"\b(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+"
    r"(?P<month>[A-Za-z]{3,9})\.?\s+(?P<year>\d{4})\b"
)
MONTH_FIRST_RE = re.compile(
    r"\b(?P<month>[A-Za-z]{3,9})\.?\s+"
    r"(?P<day>\d{1,2})(?:st|nd|rd|th)?,?\s+(?P<year>\d{4})\b"
)
ISO_DATE_RE = re.compile(r"\b(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\b")
NUMERIC_DATE_RE = re.compile(
    r"\b(?P<day>\d{1,2})[/-](?P<month>\d{1,2})[/-](?P<year>\d{4})\b"
)
ORDER_LABEL_RE = re.compile(
    r"(?i)\b(?:order(?:\s*#|\s+(?:no\.?|number))|reference|ref\.)\s*[:#-]?\s*"
    r"(?:is\s+)?(?P<value>(?=[A-Z0-9-]*\d)[A-Z0-9][A-Z0-9-]{2,})"
)
_RANGE_SEP = r"(?:\s*[-–—]\s*|\s+(?:to|and)\s+)"
RANGE_RE = re.compile(
    r"\b(?P<day1>\d{1,2})(?:st|nd|rd|th)?"
    + _RANGE_SEP
    + r"(?P<day2>\d{1,2})(?:st|nd|rd|th)?\s+"
    r"(?P<month>[A-Za-z]{3,9})\.?(?:\s+(?P<year>\d{4}))?\b"
)
MONTH_RANGE_RE = re.compile(
    r"\b(?P<month>[A-Za-z]{3,9})\.?\s+"
    r"(?P<day1>\d{1,2})(?:st|nd|rd|th)?"
    + _RANGE_SEP
    + r"(?P<day2>\d{1,2})(?:st|nd|rd|th)?"
    r"(?:,?\s+(?P<year>\d{4}))?\b"
)
ORDER_CODE_RE = re.compile(r"\b[A-Z]{2,}-\d{3,}[A-Z0-9-]*\b")
NUMBER_RE = re.compile(r"\b\d{1,3}(?:,\d{3})+(?:\.\d+)?\b|\b\d+\.\d+\b|\b\d+\b")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’]*")
NAME_WORD_RE = re.compile(
    r"[A-Z][a-z]+(?:['’][A-Z][a-z]+)?|[A-Z]['’][A-Z][a-z]+|[A-Z]{2,}"
)
NAME_JOIN_RE = re.compile(r"\s*[-–—]\s*")


_MONTH_LAST_WITHOUT_YEAR = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


def _date(day, month, year):
    try:
        found = date(int(year), int(month), int(day))
    except (TypeError, ValueError, OverflowError):
        return None
    return found.isoformat()


def _yearless_date(day, month):
    try:
        day, month = int(day), int(month)
    except (TypeError, ValueError):
        return None
    if not (1 <= month <= 12 and 1 <= day <= _MONTH_LAST_WITHOUT_YEAR[month]):
        return None
    return f"0000-{month:02d}-{day:02d}"


def _range_dates(day1, day2, month_name, year):
    month = _month_number(month_name or "")
    if month is None:
        return []
    convert = _date if year else _yearless_date
    if year:
        dates = [convert(day1, month, year), convert(day2, month, year)]
    else:
        dates = [convert(day1, month), convert(day2, month)]
    if any(item is None for item in dates):
        return []
    return dates


def _month_number(name):
    return MONTHS.get(name.lower().rstrip("."))


def _price(prefix, amount):
    try:
        value = Decimal(amount.replace(",", ""))
    except InvalidOperation:
        return None
    if "." in amount:
        value = value.quantize(Decimal("0.01"))
        rendered = f"{value:.2f}"
    else:
        rendered = str(int(value))
    symbol = {"GBP": "£", "USD": "$", "EUR": "€"}.get(prefix, prefix)
    return f"{symbol}{rendered}"


def _spans(text):
    found = []

    def add(match, kind, canonical):
        values = [canonical] if isinstance(canonical, str) else list(canonical or [])
        values = [item for item in values if item]
        if values:
            found.append((match.start(), match.end(), kind, values))

    for match in PRICE_RE.finditer(text):
        prefix = match.group("word") or match.group("symbol")
        add(match, "price", _price(prefix, match.group("amount")))
    for pattern in (RANGE_RE, MONTH_RANGE_RE):
        for match in pattern.finditer(text):
            add(match, "date", _range_dates(
                match.group("day1"), match.group("day2"),
                match.group("month"), match.group("year"),
            ))
    for match in WRITTEN_DATE_RE.finditer(text):
        month = _month_number(match.group("month"))
        add(match, "date", _date(match.group("day"), month, match.group("year")))
    for match in MONTH_FIRST_RE.finditer(text):
        month = _month_number(match.group("month"))
        add(match, "date", _date(match.group("day"), month, match.group("year")))
    for match in ISO_DATE_RE.finditer(text):
        add(match, "date", _date(match.group("day"), match.group("month"), match.group("year")))
    for match in NUMERIC_DATE_RE.finditer(text):
        add(match, "date", _date(match.group("day"), match.group("month"), match.group("year")))
    for match in ORDER_LABEL_RE.finditer(text):
        add(match, "order_id", match.group("value").upper())
    for match in ORDER_CODE_RE.finditer(text):
        add(match, "order_id", match.group(0).upper())
    found.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    accepted = []
    cursor = -1
    for start, end, kind, values in found:
        if start < cursor:
            continue
        accepted.extend((start, end, kind, canonical) for canonical in values)
        cursor = end
    return accepted


def _blank(text, spans):
    chars = list(text)
    for start, end, _kind, _canonical in spans:
        for index in range(start, end):
            chars[index] = " "
    return "".join(chars)


def _sentence_initial(text, start):
    prefix = text[:start]
    return re.search(r"(?:^|[.!?]\s+|\n\s*)$", prefix) is not None


def _names(text):
    tokens = []
    for match in WORD_RE.finditer(text):
        word = match.group(0)
        if NAME_WORD_RE.fullmatch(word) and word.lower() not in MONTHS:
            tokens.append((match.start(), match.end(), word))
    runs = []
    current = []
    for start, end, word in tokens:
        gap = text[current[-1][1]:start] if current else ""
        if current and gap.strip() and NAME_JOIN_RE.fullmatch(gap) is None:
            runs.append(current)
            current = []
        current.append((start, end, word))
    if current:
        runs.append(current)
    names = []
    for run in runs:
        if len(run) == 1 and _sentence_initial(text, run[0][0]):
            continue
        parts = [run[0][2]]
        for previous, current_word in itertools.pairwise(run):
            gap = text[previous[1]:current_word[0]]
            parts.append("-" if NAME_JOIN_RE.fullmatch(gap) else " ")
            parts.append(current_word[2])
        surface = "".join(parts)
        names.append((" ".join(surface.casefold().split()), surface))
    return names


def _numbers(text):
    values = []
    for match in NUMBER_RE.finditer(text):
        raw = match.group(0).replace(",", "")
        try:
            number = Decimal(raw)
        except InvalidOperation:
            continue
        rendered = format(number, "f").rstrip("0").rstrip(".") if "." in raw else str(int(number))
        values.append((rendered, rendered))
    return values


def extract_items(text):
    """Return (canonical, display) pairs by kind. Names keep their capitals."""
    spans = _spans(text)
    items = defaultdict(list)
    for _start, _end, kind, canonical in spans:
        items[kind].append((canonical, canonical))
    blank = _blank(text, spans)
    for canonical, surface in _names(blank):
        items["name"].append((canonical, surface))
    items["number"].extend(_numbers(blank))
    return items


def _inventory(items):
    names = sorted({surface for _canonical, surface in items["name"]}, key=str.casefold)
    return {
        "dates": sorted({canonical for canonical, _display in items["date"]}),
        "prices": sorted({canonical for canonical, _display in items["price"]}),
        "order_ids": sorted({canonical for canonical, _display in items["order_id"]}),
        "numbers": sorted(
            {canonical for canonical, _display in items["number"]},
            key=lambda value: (Decimal(value), value),
        ),
        "names": names,
    }


def _currency(value):
    for prefix in ("£", "$", "€"):
        if value.startswith(prefix):
            return prefix
    return value[:1]


def _distance(kind, left, right):
    if kind in {"number", "price"}:
        return abs(Decimal(re.sub(r"^[^\d-]+", "", left)) - Decimal(re.sub(r"^[^\d-]+", "", right)))
    if kind == "date":
        return abs(int(left.replace("-", "")) - int(right.replace("-", "")))
    return _levenshtein(left.casefold(), right.casefold())


def _levenshtein(left, right):
    if left == right:
        return 0
    previous = list(range(len(right) + 1))
    for i, left_char in enumerate(left, start=1):
        current = [i]
        for j, right_char in enumerate(right, start=1):
            current.append(min(
                current[-1] + 1,
                previous[j] + 1,
                previous[j - 1] + (left_char != right_char),
            ))
        previous = current
    return previous[-1]


def _pairable(kind, left, right):
    if kind == "price":
        return _currency(left) == _currency(right)
    if kind == "order_id":
        return _levenshtein(left, right) <= 3
    if kind == "name":
        return _levenshtein(left.casefold(), right.casefold()) <= 2
    return True


def _leftovers(source_items, candidate_items):
    source = defaultdict(list)
    candidate = defaultdict(list)
    for canonical, display in source_items:
        source[canonical].append(display)
    for canonical, display in candidate_items:
        candidate[canonical].append(display)
    missing, added = [], []
    for canonical, displays in source.items():
        overlap = min(len(displays), len(candidate.get(canonical, [])))
        missing.extend((canonical, display) for display in displays[overlap:])
    for canonical, displays in candidate.items():
        overlap = min(len(displays), len(source.get(canonical, [])))
        added.extend((canonical, display) for display in displays[overlap:])
    return missing, added


def _pair(kind, missing, added):
    pairs = []
    used = set()
    for source_index, (source_key, source_display) in enumerate(missing):
        best = None
        for added_index, (added_key, added_display) in enumerate(added):
            if added_index in used or not _pairable(kind, source_key, added_key):
                continue
            distance = _distance(kind, source_key, added_key)
            if best is None or distance < best[0]:
                best = (distance, added_index, added_display)
        if best is not None:
            used.add(best[1])
            pairs.append((source_index, source_display, best[2]))
    paired_sources = {index for index, _source, _candidate in pairs}
    return (
        [(source, candidate) for _index, source, candidate in pairs],
        [display for index, (_key, display) in enumerate(missing) if index not in paired_sources],
        [display for index, (_key, display) in enumerate(added) if index not in used],
    )


def compare(source, candidate):
    """Report facts missing, changed, or added in the candidate."""
    source_items = extract_items(source)
    candidate_items = extract_items(candidate)
    missing, changed, added = [], [], []
    for kind in ("date", "price", "order_id", "number", "name"):
        left, right = _leftovers(source_items[kind], candidate_items[kind])
        paired, still_missing, still_added = _pair(kind, left, right)
        missing.extend({"kind": kind, "value": value} for value in still_missing)
        added.extend({"kind": kind, "value": value} for value in still_added)
        changed.extend(
            {"kind": kind, "source": old, "candidate": new} for old, new in paired
        )
    missing.sort(key=lambda item: (item["kind"], item["value"]))
    changed.sort(key=lambda item: (item["kind"], item["source"], item["candidate"]))
    added.sort(key=lambda item: (item["kind"], item["value"]))
    preserved = not missing and not changed and not added
    return {
        "result": "facts_preserved" if preserved else "facts_differ",
        "missing": missing,
        "changed": changed,
        "added": added,
        "source": _inventory(source_items),
        "candidate": _inventory(candidate_items),
        "limit": LIMIT,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    try:
        report = compare(
            args.source.read_text(encoding="utf-8"),
            args.candidate.read_text(encoding="utf-8"),
        )
    except OSError as error:
        parser.exit(1, f"Fact check failed: {error}\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["result"] != "facts_preserved":
        sys.exit(1)


if __name__ == "__main__":
    main()
