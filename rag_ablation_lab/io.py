from pathlib import Path
import json

from .grid import Experiment


def read_plan(path: str) -> list[Experiment]:
    rows = []
    for line in Path(path).read_text().splitlines():
        if line.strip():
            row = json.loads(line)
            row.pop("id", None)
            rows.append(Experiment(**row))
    return rows


def read_rows(path: str) -> list[dict]:
    return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


def write_rows(path: str, rows: list[dict], append: bool = True):
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with target.open(mode, encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")
