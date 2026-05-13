#!/usr/bin/env python3
"""
extract_content.py — Content extractor for doc-to-slides skill
Supports: PDF, DOCX, PPTX, Markdown, plain text

Usage:
    python extract_content.py <file_path> [--format json|md] [--output <out_file>]

Output (JSON):
{
  "source_type": "pdf" | "docx" | "pptx" | "md" | "txt",
  "title": "Detected document title or filename",
  "language": "es" | "en" | ...,
  "detected_industry": "tech" | "finance" | "healthcare" | "education" | "legal" | "marketing" | "sustainability" | "other",
  "slide_count_hint": 12,
  "segments": [
    {
      "type": "title" | "h1" | "h2" | "h3" | "paragraph" | "bullet_list" | "numbered_list"
             | "table" | "code" | "quote" | "image_ref" | "stat_candidate" | "page_break",
      "level": 1,          // heading level (1-3), null for non-headings
      "text": "...",        // plain text content
      "items": [...],       // for lists and tables
      "rows": [[...]],      // for tables: list of rows, each row is list of cell strings
      "headers": [...],     // for tables: column header strings
      "source_page": 3,     // original page/slide number (1-indexed), null if unknown
      "notes": "..."        // speaker notes (PPTX only)
    }
  ],
  "stats": {
    "total_segments": 42,
    "headings": 8,
    "paragraphs": 14,
    "lists": 7,
    "tables": 3,
    "stat_candidates": 5,
    "images_found": 2
  },
  "warnings": ["..."]
}
"""

import sys
import os
import re
import json
import argparse
import unicodedata
from pathlib import Path
from typing import Any


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _clean(text: str) -> str:
    """Normalize unicode, strip control chars, collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f]", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def _is_likely_title(text: str) -> bool:
    words = text.split()
    return (
        1 <= len(words) <= 20
        and not text.endswith(".")
        and (text[0].isupper() if text else False)
    )


# ─────────────────────────────────────────────
# Stat / number detection
# ─────────────────────────────────────────────

STAT_PATTERNS = [
    r"\b\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s*(?:%|percent|USD|EUR|€|\$|M|B|K|mm|bn|million|billion|thousand)\b",
    r"\$\s*\d+(?:[.,]\d+)*\s*(?:M|B|K|million|billion|thousand)?\b",
    r"\b\d+(?:\.\d+)?\s*x\b",                 # 3x growth
    r"\b\d{4}\b",                              # years
    r"\b(?:increased?|decreased?|grew?|dropped?|reached?|surpassed?)\s+(?:by\s+)?\d",
]
_STAT_RE = re.compile("|".join(STAT_PATTERNS), re.IGNORECASE)

def _is_stat_candidate(text: str) -> bool:
    return bool(_STAT_RE.search(text))


# ─────────────────────────────────────────────
# Industry detection
# ─────────────────────────────────────────────

INDUSTRY_KEYWORDS = {
    "finance":        ["revenue", "ebitda", "roi", "irr", "valuation", "equity", "debt",
                       "margin", "cash flow", "investor", "balance sheet", "p&l",
                       "profit", "loss", "earnings", "dividend", "portfolio"],
    "tech":           ["api", "software", "platform", "saas", "cloud", "ai", "ml",
                       "machine learning", "neural", "model", "dataset", "algorithm",
                       "deployment", "kubernetes", "infrastructure", "latency"],
    "healthcare":     ["patient", "clinical", "diagnosis", "treatment", "drug", "therapy",
                       "biomarker", "fda", "trial", "cohort", "outcome", "hospital",
                       "physician", "pharma", "dose", "efficacy"],
    "education":      ["student", "curriculum", "learning", "course", "lesson", "teacher",
                       "syllabus", "assessment", "grade", "university", "school",
                       "pedagogy", "competency", "module", "certificate"],
    "legal":          ["contract", "clause", "liability", "compliance", "regulation",
                       "jurisdiction", "statute", "litigation", "counsel", "arbitration",
                       "gdpr", "privacy", "intellectual property", "patent", "trademark"],
    "marketing":      ["brand", "campaign", "conversion", "ctr", "funnel", "cac", "ltv",
                       "segment", "persona", "awareness", "engagement", "impressions",
                       "acquisition", "retention", "nps", "churn"],
    "sustainability": ["carbon", "emission", "esg", "renewable", "biodiversity",
                       "sustainability", "net zero", "climate", "recycling", "footprint",
                       "circular economy", "green", "solar", "wind", "scope 1"],
}

def _detect_industry(text: str) -> str:
    text_lower = text.lower()
    scores = {ind: 0 for ind in INDUSTRY_KEYWORDS}
    for ind, keywords in INDUSTRY_KEYWORDS.items():
        for kw in keywords:
            scores[ind] += len(re.findall(r"\b" + re.escape(kw) + r"\b", text_lower))
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] >= 2 else "other"


# ─────────────────────────────────────────────
# Language detection (lightweight, no deps)
# ─────────────────────────────────────────────

LANG_TOKENS = {
    "es": ["el", "la", "de", "que", "en", "los", "las", "por", "con", "para",
           "una", "del", "como", "pero", "sus", "más", "este", "esta"],
    "en": ["the", "and", "of", "to", "in", "a", "is", "that", "for", "it",
           "with", "as", "this", "are", "be", "was", "at", "by", "from"],
    "pt": ["de", "que", "o", "a", "os", "as", "em", "do", "da", "por",
           "para", "com", "uma", "não", "se", "na", "no", "ao"],
    "fr": ["le", "de", "et", "à", "les", "des", "en", "un", "une", "du",
           "que", "qui", "il", "est", "pas", "dans", "ce", "pour"],
    "de": ["der", "die", "das", "und", "in", "ist", "von", "mit", "den",
           "eine", "für", "auf", "als", "ich", "ein", "nicht", "auch"],
}

def _detect_language(text: str) -> str:
    words = re.findall(r"\b\w+\b", text.lower())
    word_set = set(words[:500])
    scores = {lang: sum(1 for t in tokens if t in word_set)
              for lang, tokens in LANG_TOKENS.items()}
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] >= 3 else "en"


# ─────────────────────────────────────────────
# Slide count heuristic
# ─────────────────────────────────────────────

def _estimate_slides(segments: list[dict]) -> int:
    h1 = sum(1 for s in segments if s["type"] in ("title", "h1"))
    h2 = sum(1 for s in segments if s["type"] == "h2")
    # Each H1 → ~1 section slide, each H2 → ~1 content slide, plus title slide
    total = 1 + h1 + h2
    # Clamp
    return max(5, min(total, 40))


# ─────────────────────────────────────────────
# Segment stats
# ─────────────────────────────────────────────

def _compute_stats(segments: list[dict]) -> dict:
    return {
        "total_segments": len(segments),
        "headings":        sum(1 for s in segments if s["type"] in ("title", "h1", "h2", "h3")),
        "paragraphs":      sum(1 for s in segments if s["type"] == "paragraph"),
        "lists":           sum(1 for s in segments if s["type"] in ("bullet_list", "numbered_list")),
        "tables":          sum(1 for s in segments if s["type"] == "table"),
        "stat_candidates": sum(1 for s in segments if s["type"] == "stat_candidate"),
        "images_found":    sum(1 for s in segments if s["type"] == "image_ref"),
        "code_blocks":     sum(1 for s in segments if s["type"] == "code"),
    }


# ─────────────────────────────────────────────
# Segment builder helpers
# ─────────────────────────────────────────────

def _seg(type_: str, text: str = "", level: int | None = None,
         items: list | None = None, rows: list | None = None,
         headers: list | None = None, page: int | None = None,
         notes: str | None = None) -> dict:
    s: dict[str, Any] = {"type": type_, "text": _clean(text)}
    if level is not None:
        s["level"] = level
    if items is not None:
        s["items"] = [_clean(i) for i in items if _clean(i)]
    if rows is not None:
        s["rows"] = [[_clean(c) for c in r] for r in rows]
    if headers is not None:
        s["headers"] = [_clean(h) for h in headers]
    if page is not None:
        s["source_page"] = page
    if notes:
        s["notes"] = _clean(notes)
    return s


def _promote_stat(seg: dict) -> dict:
    """If a paragraph contains strong stat patterns, retype it."""
    if seg["type"] == "paragraph" and _is_stat_candidate(seg["text"]):
        seg = dict(seg)
        seg["type"] = "stat_candidate"
    return seg


# ─────────────────────────────────────────────
# Markdown extractor
# ─────────────────────────────────────────────

def extract_markdown(path: Path) -> tuple[list[dict], list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    segments: list[dict] = []
    warnings: list[str] = []
    lines = text.splitlines()
    i = 0
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    first_heading_seen = False

    def flush_code():
        nonlocal in_code, code_lines, code_lang
        if code_lines:
            segments.append(_seg("code", "\n".join(code_lines)))
        code_lines = []
        code_lang = ""
        in_code = False

    while i < len(lines):
        line = lines[i]

        # Fenced code blocks
        if line.startswith("```") or line.startswith("~~~"):
            if in_code:
                flush_code()
                i += 1
                continue
            else:
                in_code = True
                code_lang = line.lstrip("`~").strip()
                i += 1
                continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue

        stripped = line.strip()
        if not stripped:
            i += 1
            continue

        # ATX headings
        hm = re.match(r"^(#{1,6})\s+(.*)", line)
        if hm:
            level = min(len(hm.group(1)), 3)
            text = _clean(hm.group(2).rstrip("#").strip())
            seg_type = "title" if not first_heading_seen and level == 1 else f"h{level}"
            if seg_type == "title" or level == 1:
                first_heading_seen = True
            segments.append(_seg(seg_type, text, level=level))
            i += 1
            continue

        # Setext headings
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if re.match(r"^={3,}$", next_line):
                text = _clean(stripped)
                seg_type = "title" if not first_heading_seen else "h1"
                first_heading_seen = True
                segments.append(_seg(seg_type, text, level=1))
                i += 2
                continue
            if re.match(r"^-{3,}$", next_line) and stripped:
                segments.append(_seg("h2", _clean(stripped), level=2))
                i += 2
                continue

        # Horizontal rule → page break hint
        if re.match(r"^(?:---|\*\*\*|___)\s*$", stripped):
            segments.append(_seg("page_break", ""))
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            quote = re.sub(r"^>\s?", "", stripped)
            segments.append(_seg("quote", quote))
            i += 1
            continue

        # Unordered list — collect consecutive items
        if re.match(r"^[-*+]\s", stripped):
            items = []
            while i < len(lines):
                l = lines[i].strip()
                if re.match(r"^[-*+]\s", l):
                    items.append(re.sub(r"^[-*+]\s+", "", l))
                    i += 1
                elif l == "":
                    i += 1
                    break
                else:
                    break
            segments.append(_seg("bullet_list", "", items=items))
            continue

        # Ordered list
        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < len(lines):
                l = lines[i].strip()
                if re.match(r"^\d+\.\s", l):
                    items.append(re.sub(r"^\d+\.\s+", "", l))
                    i += 1
                elif l == "":
                    i += 1
                    break
                else:
                    break
            segments.append(_seg("numbered_list", "", items=items))
            continue

        # GFM table
        if "|" in stripped and i + 1 < len(lines) and re.match(r"^\|?\s*[-:]+\s*\|", lines[i + 1]):
            header_row = [c.strip() for c in stripped.strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and "|" in lines[j]:
                row = [c.strip() for c in lines[j].strip("|").split("|")]
                rows.append(row)
                j += 1
            segments.append(_seg("table", "", headers=header_row, rows=rows))
            i = j
            continue

        # Image reference
        if re.match(r"^!\[", stripped):
            alt = re.search(r"!\[([^\]]*)\]", stripped)
            segments.append(_seg("image_ref", alt.group(1) if alt else "image"))
            i += 1
            continue

        # Paragraph — collect until blank line
        para_lines = []
        while i < len(lines) and lines[i].strip():
            para_lines.append(lines[i].strip())
            i += 1
        para = " ".join(para_lines)
        seg = _seg("paragraph", para)
        segments.append(_promote_stat(seg))

    if in_code:
        flush_code()

    return segments, warnings


# ─────────────────────────────────────────────
# Plain text extractor
# ─────────────────────────────────────────────

def extract_txt(path: Path) -> tuple[list[dict], list[str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    segments: list[dict] = []
    warnings: list[str] = []
    blocks = re.split(r"\n{2,}", text)
    first = True

    for block in blocks:
        block = _clean(block)
        if not block:
            continue

        lines = block.splitlines()

        # Short single line → likely a heading
        if len(lines) == 1 and len(block) <= 80 and _is_likely_title(block):
            if first:
                segments.append(_seg("title", block, level=1))
                first = False
            else:
                segments.append(_seg("h2", block, level=2))
            continue

        # All-caps line → section heading
        if len(lines) == 1 and block.isupper() and len(block) < 60:
            segments.append(_seg("h2", block.title(), level=2))
            continue

        # Bullet-like lines
        bullet_lines = [l.strip() for l in lines if re.match(r"^[-•*·]\s", l.strip())]
        if len(bullet_lines) >= len(lines) * 0.7 and len(bullet_lines) >= 2:
            items = [re.sub(r"^[-•*·]\s+", "", l) for l in bullet_lines]
            segments.append(_seg("bullet_list", "", items=items))
            continue

        # Numbered list
        num_lines = [l.strip() for l in lines if re.match(r"^\d+[.)]\s", l.strip())]
        if len(num_lines) >= len(lines) * 0.7 and len(num_lines) >= 2:
            items = [re.sub(r"^\d+[.)]\s+", "", l) for l in num_lines]
            segments.append(_seg("numbered_list", "", items=items))
            continue

        seg = _seg("paragraph", block)
        segments.append(_promote_stat(seg))
        first = False

    return segments, warnings


# ─────────────────────────────────────────────
# DOCX extractor
# ─────────────────────────────────────────────

def extract_docx(path: Path) -> tuple[list[dict], list[str]]:
    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError:
        return [], ["python-docx not installed. Run: pip install python-docx"]

    doc = Document(str(path))
    segments: list[dict] = []
    warnings: list[str] = []
    first_heading = True

    HEADING_MAP = {
        "heading 1": ("h1", 1),
        "heading 2": ("h2", 2),
        "heading 3": ("h3", 3),
        "heading 4": ("h3", 3),
        "title":     ("title", 1),
        "subtitle":  ("h2", 2),
    }

    def table_to_seg(tbl):
        rows = []
        for i, row in enumerate(tbl.rows):
            cells = [_clean(cell.text) for cell in row.cells]
            rows.append(cells)
        if not rows:
            return None
        headers = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else rows
        return _seg("table", "", headers=headers, rows=data_rows)

    # Tables by paragraph index — collect them
    table_index: dict[int, Any] = {}
    try:
        body_xml = doc.element.body
        idx = 0
        for child in body_xml.iterchildren():
            tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag == "tbl":
                # find docx table object
                for t in doc.tables:
                    if t._element is child:
                        table_index[idx] = t
                        break
            idx += 1
    except Exception:
        pass

    pending_list_items: list[str] = []
    pending_list_type: str = "bullet_list"

    def flush_list():
        nonlocal pending_list_items, pending_list_type
        if pending_list_items:
            segments.append(_seg(pending_list_type, "", items=list(pending_list_items)))
            pending_list_items = []

    for para in doc.paragraphs:
        text = _clean(para.text)
        if not text:
            continue

        style_name = para.style.name.lower() if para.style and para.style.name else ""

        # Heading
        if style_name in HEADING_MAP:
            flush_list()
            seg_type, level = HEADING_MAP[style_name]
            if seg_type == "h1" and first_heading:
                seg_type = "title"
                first_heading = False
            elif seg_type == "title":
                first_heading = False
            segments.append(_seg(seg_type, text, level=level))
            continue

        # List paragraph
        if "list" in style_name:
            flush_list()
            is_numbered = "number" in style_name or "enum" in style_name
            pending_list_type = "numbered_list" if is_numbered else "bullet_list"
            pending_list_items.append(text)
            continue

        # Check numPr (XML list marker)
        try:
            numPr = para._element.find(qn("w:pPr"))
            if numPr is not None and numPr.find(qn("w:numPr")) is not None:
                pending_list_items.append(text)
                continue
        except Exception:
            pass

        flush_list()

        seg = _seg("paragraph", text)
        segments.append(_promote_stat(seg))

    flush_list()

    # Insert tables from doc.tables (append at end if not already indexed)
    for tbl in doc.tables:
        seg = table_to_seg(tbl)
        if seg:
            segments.append(seg)

    # Inline images hint
    try:
        from docx.oxml.ns import nsmap
    except Exception:
        pass

    try:
        rels = [r for r in doc.part.rels.values()
                if "image" in r.reltype]
        if rels:
            segments.append(_seg("image_ref", f"{len(rels)} image(s) in document"))
    except Exception:
        pass

    return segments, warnings


# ─────────────────────────────────────────────
# PDF extractor
# ─────────────────────────────────────────────

def extract_pdf(path: Path) -> tuple[list[dict], list[str]]:
    warnings: list[str] = []

    # Try pdfplumber first (best for text + tables)
    try:
        import pdfplumber
        return _extract_pdf_pdfplumber(path, warnings)
    except ImportError:
        warnings.append("pdfplumber not found, trying PyMuPDF...")

    # Fallback: PyMuPDF (fitz)
    try:
        import fitz
        return _extract_pdf_pymupdf(path, warnings)
    except ImportError:
        warnings.append("PyMuPDF (fitz) not found, trying pypdf...")

    # Fallback: pypdf
    try:
        from pypdf import PdfReader
        return _extract_pdf_pypdf(path, warnings)
    except ImportError:
        pass

    # Last resort: pdfminer
    try:
        return _extract_pdf_pdfminer(path, warnings)
    except ImportError:
        pass

    return [], warnings + ["No PDF library found. Install one of: pdfplumber, PyMuPDF, pypdf, pdfminer.six"]


def _extract_pdf_pdfplumber(path: Path, warnings: list) -> tuple[list[dict], list[str]]:
    import pdfplumber

    segments: list[dict] = []
    first_page = True

    with pdfplumber.open(str(path)) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):

            # Tables first
            tables = page.extract_tables()
            extracted_table_bboxes = []
            for tbl in tables:
                if not tbl or not tbl[0]:
                    continue
                headers = [_clean(str(c)) if c else "" for c in tbl[0]]
                rows = [[_clean(str(c)) if c else "" for c in row] for row in tbl[1:]]
                segments.append(_seg("table", "", headers=headers, rows=rows, page=page_num))
                extracted_table_bboxes.append(True)

            # Text (filter out table regions if possible)
            text = page.extract_text(x_tolerance=3, y_tolerance=3) or ""
            if not text.strip():
                continue

            lines = text.splitlines()
            para_lines: list[str] = []

            def flush_para():
                nonlocal para_lines
                if para_lines:
                    block = " ".join(para_lines).strip()
                    if block:
                        seg = _seg("paragraph", block, page=page_num)
                        segments.append(_promote_stat(seg))
                    para_lines = []

            for line in lines:
                line = _clean(line)
                if not line:
                    flush_para()
                    continue

                # Font size heuristic: ALL CAPS short line → heading
                if line.isupper() and len(line.split()) <= 8 and len(line) < 60:
                    flush_para()
                    if first_page and not segments:
                        segments.append(_seg("title", line.title(), level=1, page=page_num))
                        first_page = False
                    else:
                        segments.append(_seg("h2", line.title(), level=2, page=page_num))
                    continue

                # Short capitalized line that looks like a heading
                if _is_likely_title(line) and len(line.split()) <= 10 and not para_lines:
                    flush_para()
                    if not segments and first_page:
                        segments.append(_seg("title", line, level=1, page=page_num))
                        first_page = False
                    else:
                        segments.append(_seg("h2", line, level=2, page=page_num))
                    continue

                # Bullet line
                if re.match(r"^[•·▪▸►‣‐‒–—\-]\s", line) or re.match(r"^\d+\.\s", line):
                    flush_para()
                    is_num = bool(re.match(r"^\d+\.\s", line))
                    item = re.sub(r"^[•·▪▸►‣\-\d.]\s+", "", line)
                    # Check if we can append to previous list
                    if segments and segments[-1]["type"] in ("bullet_list", "numbered_list"):
                        target_type = "numbered_list" if is_num else "bullet_list"
                        if segments[-1]["type"] == target_type:
                            segments[-1]["items"].append(_clean(item))
                            continue
                    list_type = "numbered_list" if is_num else "bullet_list"
                    segments.append(_seg(list_type, "", items=[item], page=page_num))
                    continue

                para_lines.append(line)

            flush_para()

    return segments, warnings


def _extract_pdf_pymupdf(path: Path, warnings: list) -> tuple[list[dict], list[str]]:
    import fitz

    segments: list[dict] = []
    doc = fitz.open(str(path))

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict", flags=fitz.TEXT_PRESERVE_WHITESPACE)["blocks"]

        for block in blocks:
            if block.get("type") != 0:  # 0 = text
                if block.get("type") == 1:
                    segments.append(_seg("image_ref", f"image on page {page_num}", page=page_num))
                continue

            lines_text = []
            avg_size = 0.0
            sizes = []

            for line in block.get("lines", []):
                line_str = ""
                for span in line.get("spans", []):
                    line_str += span.get("text", "")
                    sizes.append(span.get("size", 11))
                lines_text.append(_clean(line_str))

            block_text = " ".join(t for t in lines_text if t)
            if not block_text:
                continue

            if sizes:
                avg_size = sum(sizes) / len(sizes)

            # Large font = heading
            if avg_size > 15 and len(block_text.split()) <= 15:
                if not segments:
                    segments.append(_seg("title", block_text, level=1, page=page_num))
                elif avg_size > 18:
                    segments.append(_seg("h1", block_text, level=1, page=page_num))
                else:
                    segments.append(_seg("h2", block_text, level=2, page=page_num))
                continue

            # Medium heading
            if avg_size > 12.5 and len(block_text.split()) <= 12:
                segments.append(_seg("h3", block_text, level=3, page=page_num))
                continue

            seg = _seg("paragraph", block_text, page=page_num)
            segments.append(_promote_stat(seg))

    doc.close()
    return segments, warnings


def _extract_pdf_pypdf(path: Path, warnings: list) -> tuple[list[dict], list[str]]:
    from pypdf import PdfReader

    segments: list[dict] = []
    reader = PdfReader(str(path))
    first = True

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        if not text.strip():
            continue
        blocks = re.split(r"\n{2,}", text)
        for block in blocks:
            block = _clean(block)
            if not block:
                continue
            lines = block.splitlines()
            if len(lines) == 1 and _is_likely_title(block) and len(block) < 80:
                if first:
                    segments.append(_seg("title", block, level=1, page=page_num))
                    first = False
                else:
                    segments.append(_seg("h2", block, level=2, page=page_num))
                continue
            seg = _seg("paragraph", block, page=page_num)
            segments.append(_promote_stat(seg))
            first = False

    return segments, warnings


def _extract_pdf_pdfminer(path: Path, warnings: list) -> tuple[list[dict], list[str]]:
    from pdfminer.high_level import extract_text as pm_extract

    text = pm_extract(str(path))
    segments, w = extract_txt.__wrapped__(path, text) if hasattr(extract_txt, "__wrapped__") else _txt_from_string(text)
    warnings.extend(w)
    return segments, warnings


def _txt_from_string(text: str) -> tuple[list[dict], list[str]]:
    import tempfile
    tmp = Path(tempfile.mktemp(suffix=".txt"))
    tmp.write_text(text, encoding="utf-8")
    segs, warns = extract_txt(tmp)
    tmp.unlink(missing_ok=True)
    return segs, warns


# ─────────────────────────────────────────────
# PPTX extractor (convert existing PPTX → segments)
# ─────────────────────────────────────────────

def extract_pptx(path: Path) -> tuple[list[dict], list[str]]:
    try:
        from pptx import Presentation
        from pptx.util import Pt
        from pptx.enum.text import PP_ALIGN
    except ImportError:
        return [], ["python-pptx not installed. Run: pip install python-pptx"]

    prs = Presentation(str(path))
    segments: list[dict] = []
    warnings: list[str] = []
    first_slide = True

    for slide_num, slide in enumerate(prs.slides, start=1):
        slide_title = None
        slide_body_segments: list[dict] = []
        slide_notes = ""

        # Speaker notes
        try:
            notes_slide = slide.notes_slide
            notes_tf = notes_slide.notes_text_frame
            slide_notes = _clean(notes_tf.text) if notes_tf else ""
        except Exception:
            pass

        for shape in slide.shapes:
            if not shape.has_text_frame:
                # Image?
                try:
                    if shape.shape_type == 13:  # MSO_SHAPE_TYPE.PICTURE
                        slide_body_segments.append(
                            _seg("image_ref", f"image in slide {slide_num}", page=slide_num)
                        )
                except Exception:
                    pass
                # Table?
                try:
                    if shape.has_table:
                        tbl = shape.table
                        rows = []
                        for row in tbl.rows:
                            rows.append([_clean(cell.text_frame.text) for cell in row.cells])
                        headers = rows[0] if rows else []
                        data_rows = rows[1:] if len(rows) > 1 else []
                        slide_body_segments.append(
                            _seg("table", "", headers=headers, rows=data_rows, page=slide_num)
                        )
                except Exception:
                    pass
                continue

            tf = shape.text_frame
            is_title_placeholder = False

            try:
                from pptx.util import Emu
                ph = shape.placeholder_format
                if ph is not None and ph.idx in (0, 1):
                    is_title_placeholder = True
            except Exception:
                pass

            # Determine text and font size
            full_text = _clean(tf.text)
            if not full_text:
                continue

            max_size = 0
            for para in tf.paragraphs:
                for run in para.runs:
                    try:
                        if run.font.size:
                            sz = run.font.size.pt
                            if sz > max_size:
                                max_size = sz
                    except Exception:
                        pass

            if is_title_placeholder or max_size >= 24:
                slide_title = full_text
                continue

            # Collect list items
            items = []
            for para in tf.paragraphs:
                pt = _clean(para.text)
                if pt:
                    items.append(pt)

            if len(items) > 1:
                slide_body_segments.append(
                    _seg("bullet_list", "", items=items, page=slide_num)
                )
            elif items:
                seg = _seg("paragraph", items[0], page=slide_num)
                slide_body_segments.append(_promote_stat(seg))

        # Emit title heading for this slide
        if slide_title:
            if first_slide:
                segments.append(_seg("title", slide_title, level=1, page=slide_num,
                                     notes=slide_notes if slide_notes else None))
                first_slide = False
            else:
                segments.append(_seg("h2", slide_title, level=2, page=slide_num,
                                     notes=slide_notes if slide_notes else None))

        segments.extend(slide_body_segments)

    return segments, warnings


# ─────────────────────────────────────────────
# Dispatch
# ─────────────────────────────────────────────

EXTRACTORS = {
    ".md":   extract_markdown,
    ".markdown": extract_markdown,
    ".txt":  extract_txt,
    ".text": extract_txt,
    ".pdf":  extract_pdf,
    ".docx": extract_docx,
    ".doc":  extract_docx,
    ".pptx": extract_pptx,
    ".ppt":  extract_pptx,
}


def extract(path: str | Path) -> dict:
    path = Path(path)
    if not path.exists():
        return {"error": f"File not found: {path}"}

    ext = path.suffix.lower()
    extractor = EXTRACTORS.get(ext)
    if extractor is None:
        return {"error": f"Unsupported file type: {ext}. Supported: {', '.join(EXTRACTORS.keys())}"}

    segments, warnings = extractor(path)

    # Remove empty segments
    segments = [s for s in segments if s.get("text") or s.get("items") or s.get("rows")]

    # Full text for meta-analysis
    all_text = " ".join(
        s.get("text", "") + " " + " ".join(s.get("items", []))
        for s in segments
    )

    # Title detection
    title = ""
    for s in segments:
        if s["type"] in ("title", "h1") and s.get("text"):
            title = s["text"]
            break
    if not title:
        title = path.stem.replace("_", " ").replace("-", " ").title()

    source_type = ext.lstrip(".")
    if source_type in ("markdown",):
        source_type = "md"
    if source_type in ("doc",):
        source_type = "docx"
    if source_type in ("ppt",):
        source_type = "pptx"
    if source_type in ("text",):
        source_type = "txt"

    return {
        "source_type":       source_type,
        "title":             title,
        "language":          _detect_language(all_text),
        "detected_industry": _detect_industry(all_text),
        "slide_count_hint":  _estimate_slides(segments),
        "segments":          segments,
        "stats":             _compute_stats(segments),
        "warnings":          warnings,
    }


# ─────────────────────────────────────────────
# Markdown output helper
# ─────────────────────────────────────────────

def segments_to_markdown(result: dict) -> str:
    lines = []
    title = result.get("title", "Document")
    lines.append(f"# {title}\n")
    lines.append(f"> **Source:** {result.get('source_type','?').upper()}  |  "
                 f"**Language:** {result.get('language','?')}  |  "
                 f"**Industry:** {result.get('detected_industry','?')}  |  "
                 f"**Estimated slides:** {result.get('slide_count_hint','?')}\n")

    for seg in result.get("segments", []):
        t = seg["type"]
        text = seg.get("text", "")
        items = seg.get("items", [])
        rows = seg.get("rows", [])
        headers = seg.get("headers", [])

        if t == "title":
            lines.append(f"\n# {text}\n")
        elif t == "h1":
            lines.append(f"\n# {text}\n")
        elif t == "h2":
            lines.append(f"\n## {text}\n")
        elif t == "h3":
            lines.append(f"\n### {text}\n")
        elif t in ("paragraph", "stat_candidate", "quote"):
            prefix = "> " if t == "quote" else ""
            lines.append(f"\n{prefix}{text}\n")
        elif t == "bullet_list":
            lines.append("")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")
        elif t == "numbered_list":
            lines.append("")
            for i, item in enumerate(items, 1):
                lines.append(f"{i}. {item}")
            lines.append("")
        elif t == "table":
            lines.append("")
            if headers:
                lines.append("| " + " | ".join(headers) + " |")
                lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in rows:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")
        elif t == "code":
            lines.append(f"\n```\n{text}\n```\n")
        elif t == "image_ref":
            lines.append(f"\n_[Image: {text}]_\n")
        elif t == "page_break":
            lines.append("\n---\n")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Extract structured content from PDF, DOCX, PPTX, Markdown, or TXT files."
    )
    parser.add_argument("file", help="Path to input file")
    parser.add_argument(
        "--format", choices=["json", "md"], default="json",
        help="Output format: json (default) or md (Markdown preview)"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output file path. If not set, prints to stdout."
    )
    parser.add_argument(
        "--pretty", action="store_true",
        help="Pretty-print JSON output (indented)"
    )

    args = parser.parse_args()

    result = extract(args.file)

    if "error" in result:
        print(f"ERROR: {result['error']}", file=sys.stderr)
        sys.exit(1)

    if args.format == "md":
        output = segments_to_markdown(result)
    else:
        indent = 2 if args.pretty else None
        output = json.dumps(result, ensure_ascii=False, indent=indent)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"✓ Written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
