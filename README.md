# jsonlq

Tiny dependency-free Python CLI for querying JSONL. Handy for quick log inspection without jq.

## Install
Copy `jsonlq.py` somewhere on your PATH (Python 3.8+).

## Usage
    python jsonlq.py data.jsonl --where status=ok --select user.id,ms
    cat data.jsonl | python jsonlq.py --count --where level=error
    python jsonlq.py data.jsonl --stats ms   # {"count":..,"min":..,"max":..,"mean":..}

Options: `--select a.b,c` (dotted paths, list indexes allowed), `--where key=value` (repeatable, ANDed), `--count`, `--stats FIELD`.

## Tests
    python -m venv .venv && .venv/bin/pip install pytest && .venv/bin/pytest

MIT licensed.
