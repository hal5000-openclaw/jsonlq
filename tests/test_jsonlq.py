import io, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import jsonlq

DATA = '{"a":{"b":1},"c":"x","n":2}\n\n{"a":{"b":2},"c":"y","n":4}\n'

def run(args, capsys):
    rc = jsonlq.main(args, io.StringIO(DATA))
    return rc, capsys.readouterr().out

def test_select(capsys):
    _, out = run(["--select", "a.b,c"], capsys)
    assert [json.loads(l) for l in out.splitlines()] == [{"a.b": 1, "c": "x"}, {"a.b": 2, "c": "y"}]

def test_where_count(capsys):
    assert run(["--where", "c=y", "--count"], capsys)[1] == "1\n"
    assert run(["--where", "a.b=1", "--count"], capsys)[1] == "1\n"

def test_stats(capsys):
    _, out = run(["--stats", "n"], capsys)
    assert json.loads(out) == {"count": 2, "min": 2, "max": 4, "mean": 3.0}

def test_bad_json(capsys):
    assert jsonlq.main([], io.StringIO("{oops\n")) == 1
