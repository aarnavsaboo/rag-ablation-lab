from argparse import ArgumentParser
from pathlib import Path
import json

from .grid import expand_grid, paired_delta


def _scores(path: str) -> list[float]:
    return [json.loads(x)["ndcg"] for x in Path(path).read_text().splitlines() if x.strip()]


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    grid = sub.add_parser("grid")
    grid.add_argument("config")
    compare = sub.add_parser("compare")
    compare.add_argument("left")
    compare.add_argument("right")
    args = parser.parse_args()

    if args.cmd == "grid":
        config = json.loads(Path(args.config).read_text())
        for exp in expand_grid(config):
            print(json.dumps({"id": exp.id, **exp.__dict__}, sort_keys=True))
    else:
        print(json.dumps(paired_delta(_scores(args.left), _scores(args.right)), indent=2))


if __name__ == "__main__":
    main()
