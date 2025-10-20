import json
import sys
import re
import subprocess
from typing import List, Dict, Any

try:
    # Prefer the Python client if available and returns useful data
    import ollama
    try:
        res = ollama.list()
        # If the client returned something empty or not helpful, fall back to CLI
        if res:
            print(json.dumps(res, indent=2))
            raise SystemExit(0)
    except Exception:
        # fall back to CLI parsing below
        pass
except Exception:
    # no python client installed, fall back to CLI
    pass


_TIMESTAMP_RE = re.compile(r'^(?:\d{1,4}-\d{1,2}-\d{1,2}|\d{1,2}:\d{2}:\d{2}(?:\.\d+)?(?:[+-]\d{2}:\d{2})?)$')


def parse_ollama_list_output(text: str) -> List[Dict[str, Any]]:
    """Parse the textual output of `ollama list` (table format) into list of dicts.

    Handles noisy lines (timestamps), variable spacing, and missing fields.
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    # Filter out empty lines and lines that look like lone timestamps
    lines = [ln for ln in lines if ln.strip() and not _TIMESTAMP_RE.match(ln.strip())]

    # Find header line that starts with NAME and contains SIZE (best-effort)
    header_idx = None
    for i, ln in enumerate(lines):
        if ln.strip().upper().startswith('NAME') and 'SIZE' in ln.upper():
            header_idx = i
            break
    if header_idx is None:
        return []

    header_line = lines[header_idx]
    # Data rows start after the separator line (---) if present
    start_idx = header_idx + 1
    if start_idx < len(lines) and re.match(r'^[-\s]+$', lines[start_idx]):
        start_idx += 1

    headers = re.split(r'\s{2,}', header_line.strip())
    entries: List[Dict[str, Any]] = []

    for ln in lines[start_idx:]:
        # Stop if another header-like block appears
        if ln.strip().upper().startswith('NAME') and 'SIZE' in ln.upper():
            break
        # Split on two or more spaces to respect values containing single spaces
        parts = re.split(r'\s{2,}', ln.strip())
        # If there are more parts than headers, join the extras into the last column
        if len(parts) > len(headers):
            parts = parts[: len(headers) - 1] + ['  '.join(parts[len(headers) - 1:])]

        # Map parts to headers
        row: Dict[str, Any] = {}
        for i, h in enumerate(headers):
            row[h] = parts[i] if i < len(parts) else ''
        entries.append(row)

    return entries


def run_cli_list() -> str:
    """Run `ollama list` CLI and return its stdout as text.

    This avoids depending on the python client and works even if the client returns
    incomplete data.
    """
    try:
        cp = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=False)
        out = cp.stdout or cp.stderr or ''
        return out
    except FileNotFoundError as e:
        print('ERROR: ollama CLI not found in PATH:', e)
        sys.exit(1)


if __name__ == '__main__':
    raw = run_cli_list()
    parsed = parse_ollama_list_output(raw)
    if parsed:
        print(json.dumps(parsed, indent=2))
    else:
        # If parsing failed, dump raw output for debugging
        print(raw)
