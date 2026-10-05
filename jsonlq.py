#!/usr/bin/env python3
"""jsonlq: tiny JSONL query tool."""
import argparse, json, sys


def get_path(obj, path):
    for part in path.split("."):
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        elif isinstance(obj, list) and part.isdigit() and int(part) < len(obj):
            obj = obj[int(part)]
        else:
            return None
    return obj


def matches(rec, where):
    for k, v in where:
        val = get_path(rec, k)
        if not (str(val) == v or json.dumps(val) == v):
            return False
    return True


def main(argv=None, stdin=None):
    p = argparse.ArgumentParser(prog="jsonlq", description="Query JSONL files.")
    p.add_argument("file", nargs="?", help="input file (default: stdin)")
    p.add_argument("--select", help="comma-separated dotted paths")
    p.add_argument("--where", action="append", default=[], help="key=value (repeatable)")
    p.add_argument("--count", action="store_true", help="print number of matching records")
    p.add_argument("--stats", metavar="FIELD", help="min/max/mean of numeric field")
    a = p.parse_args(argv)
    where = []
    for w in a.where:
        if "=" not in w:
            p.error("--where needs key=value")
        where.append(tuple(w.split("=", 1)))
    src = open(a.file) if a.file else (stdin or sys.stdin)
    recs = []
    for n, line in enumerate(src, 1):
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except ValueError:
            print(f"jsonlq: line {n}: invalid JSON", file=sys.stderr)
            return 1
        if matches(rec, where):
            recs.append(rec)
    if a.count:
        print(len(recs))
    elif a.stats:
        nums = [x for x in (get_path(r, a.stats) for r in recs)
                if isinstance(x, (int, float)) and not isinstance(x, bool)]
        if not nums:
            print("jsonlq: no numeric values", file=sys.stderr)
            return 1
        print(json.dumps({"count": len(nums), "min": min(nums),
                          "max": max(nums), "mean": sum(nums) / len(nums)}))
    else:
        fields = a.select.split(",") if a.select else None
        for r in recs:
            print(json.dumps({f: get_path(r, f) for f in fields} if fields else r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
