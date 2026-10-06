# jsonlq

Tiny dependency-free Python CLI for querying JSONL. Handy for quick log inspection without jq.

## Install
Copy `jsonlq.py` somewhere on your PATH (Python 3.8+).

## Usage
    python jsonlq.py data.jsonl --where status=ok --select user.id,ms
    cat data.jsonl | python jsonlq.py --count --where level=error
    python jsonlq.py data.jsonl --stats ms   # {"count":..,"min":..,"max":..,"mean":..}

Options: `--select a.b,c` (dotted paths, list indexes allowed), `--where key=value` (repeatable, ANDed), `--count`, `--stats FIELD`.

## Example
Given `{"user":{"id":1},"ms":10,"status":"ok"}` and `{"user":{"id":2},"ms":30,"status":"err"}`:

    $ jsonlq.py s.jsonl --where status=ok --select user.id,ms
    {"user.id": 1, "ms": 10}
    $ jsonlq.py s.jsonl --stats ms
    {"count": 2, "min": 10, "max": 30, "mean": 20.0}

## Tests
    python -m venv .venv && .venv/bin/pip install pytest && .venv/bin/pytest

MIT licensed.
