#!/usr/bin/env python3
"""
Simple SRT validator.

Usage:
    python validate_srt.py subtitle.srt

Checks:
    - Sequence numbers present and in increasing order (flags gaps/dupes)
    - Timestamp line format (00:00:00,000 --> 00:00:00,000)
    - Start time strictly before end time within a block
    - Blocks in chronological order (no overlaps, no out-of-order starts)
    - No empty subtitle text
    - No blank line missing between blocks (basic structural check)
"""

import re
import sys
from analysis import get_input_files

TIME_RE = re.compile(
    r'^(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*$'
)
 
 
def time_to_ms(h, m, s, ms):
    return ((int(h) * 3600 + int(m) * 60 + int(s)) * 1000) + int(ms)
 
 
def parse_timestamp_line(line):
    match = TIME_RE.match(line)
    if not match:
        return None
    h1, m1, s1, ms1, h2, m2, s2, ms2 = match.groups()
    start = time_to_ms(h1, m1, s1, ms1)
    end = time_to_ms(h2, m2, s2, ms2)
    return start, end
 
 
def check_line_endings(raw_text):
    """Detect line ending style and flag anything other than clean CRLF or LF."""
    warnings = []
 
    has_crlf = '\r\n' in raw_text
    # Bare \r not part of a \r\n pair (old classic Mac style)
    bare_cr = re.search(r'\r(?!\n)', raw_text) is not None
 
    if bare_cr:
        warnings.append(
            "File contains bare '\\r' (old Mac-style) line endings. "
            "Many players/editors mishandle these — convert to CRLF or LF."
        )
    if has_crlf and not bare_cr:
        # Check if it's consistently CRLF, or a mix of CRLF and bare LF
        lf_count = raw_text.count('\n')
        crlf_count = raw_text.count('\r\n')
        if lf_count != crlf_count:
            warnings.append(
                "File has mixed line endings (some CRLF, some bare LF). "
                "Consider normalizing to one style."
            )
 
    return warnings
 
 
def split_blocks(raw_text):
    # Normalize line endings (handles \r\n and bare \r)
    text = raw_text.replace('\r\n', '\n').replace('\r', '\n')
    # Blocks are separated by one or more blank lines
    raw_blocks = re.split(r'\n\s*\n', text.strip())
    return raw_blocks
 
 
def validate(input_file):
    errors = []
    warnings = []
 
    with open(input_file, 'rb') as f:
        raw_bytes = f.read()
    raw_text = raw_bytes.decode('utf-8-sig', errors='replace')
 
    warnings.extend(check_line_endings(raw_text))
 
    raw_blocks = split_blocks(raw_text)
 
    if not raw_blocks or raw_blocks == ['']:
        errors.append("File appears to be empty.")
        return errors, warnings
 
    parsed_blocks = []
    expected_seq = 1
 
    for block_num, raw_block in enumerate(raw_blocks, start=1):
        lines = [ln for ln in raw_block.split('\n')]
        # Strip trailing empty lines within a block
        while lines and lines[-1].strip() == '':
            lines.pop()
 
        if len(lines) < 2:
            errors.append(
                f"Block #{block_num}: malformed block, expected at least a "
                f"sequence number and a timestamp line, got {len(lines)} line(s)."
            )
            continue
 
        # --- Sequence number ---
        seq_line = lines[0].strip()
        if not seq_line.isdigit():
            errors.append(
                f"Block #{block_num}: expected a numeric sequence number, "
                f"found '{seq_line}'."
            )
            seq_num = None
        else:
            seq_num = int(seq_line)
            if seq_num != expected_seq:
                warnings.append(
                    f"Block #{block_num}: sequence number {seq_num} "
                    f"(expected {expected_seq})."
                )
            expected_seq = seq_num + 1 if seq_num is not None else expected_seq + 1
 
        # --- Timestamp line ---
        if len(lines) < 2:
            continue
        ts_line = lines[1].strip()
        parsed_ts = parse_timestamp_line(ts_line)
        if parsed_ts is None:
            errors.append(
                f"Block #{block_num}: invalid timestamp format: '{ts_line}' "
                f"(expected 00:00:00,000 --> 00:00:00,000)."
            )
            continue
 
        start_ms, end_ms = parsed_ts
        if start_ms >= end_ms:
            errors.append(
                f"Block #{block_num} (seq {seq_num}): start time is not "
                f"before end time ({ts_line})."
            )
 
        # --- Text content ---
        text_lines = lines[2:]
        joined_text = '\n'.join(text_lines).strip()
        if not joined_text:
            errors.append(f"Block #{block_num} (seq {seq_num}): empty subtitle text.")
 
        parsed_blocks.append({
            'block_num': block_num,
            'seq_num': seq_num,
            'start_ms': start_ms,
            'end_ms': end_ms,
            'text': joined_text,
        })
 
    # --- Chronological order / overlap checks ---
    for i in range(1, len(parsed_blocks)):
        prev = parsed_blocks[i - 1]
        curr = parsed_blocks[i]
        if curr['start_ms'] < prev['start_ms']:
            errors.append(
                f"Block #{curr['block_num']} (seq {curr['seq_num']}): starts "
                f"before previous block #{prev['block_num']} (seq {prev['seq_num']})."
            )
        if curr['start_ms'] < prev['end_ms']:
            errors.append(
                f"Block #{curr['block_num']} (seq {curr['seq_num']}): overlaps "
                f"with previous block #{prev['block_num']} (seq {prev['seq_num']})."
            )
 
    return errors, warnings

def main():
    input_files = get_input_files(filetypes = [("SRT Files", "*.srt")])    
    for input_file in input_files:
        errors, warnings = validate(input_file)
        if not errors and not warnings:
            print(f"OK: no issues found in {input_file}")
            sys.exit(0)
        if errors:
            print(f"Found {len(errors)} error(s):")
            for e in errors:
                print(f"  ERROR: {e}")
        if warnings:
            print(f"Found {len(warnings)} warning(s):")
            for w in warnings:
                print(f"  WARNING: {w}")

        sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
