from argparse import ArgumentParser
from pathlib import Path
import json

from .dataset import load
from .grid import expand_grid
from .io import read_plan, read_rows, write_rows
from .report import summarize
from .runner import run_experiment
from .stats import paired_records


def main():
    parser = ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    grid = sub.add_parser("grid")
    grid.add_argument("config")

    run = sub.add_parser("run")
    run.add_argument("plan")
    run.add_argument("--dataset", required=True)
    run.add_argument("--out", required=True)

    summary = sub.add_parser("summarize")
    summary.add_argument("path")

    compare = sub.add_parser("compare")
    compare.add_argument("path")
    compare.add_argument("left")
    compare.add_argument("right")
    compare.add_argument("--metric", choices=["recall","mrr","ndcg"], default="ndcg")

    args = parser.parse_args()

    if args.cmd == "grid":
        config = json.loads(Path(args.config).read_text())
        for exp in expand_grid(config):
            print(json.dumps({"id":exp.id, **exp.__dict__}, sort_keys=True))
    elif args.cmd == "run":
        dataset = load(args.dataset)
        all_rows = []
        for exp in read_plan(args.plan):
            try:
                all_rows.extend(run_experiment(dataset, exp))
            except NotImplementedError as exc:
                all_rows.append({"experiment_id":exp.id,"skipped":True,"reason":str(exc),"config":exp.__dict__})
        write_rows(args.out, all_rows, append=False)
        print(json.dumps({"records":len(all_rows)}))
    elif args.cmd == "summarize":
        rows = [x for x in read_rows(args.path) if not x.get("skipped")]
        print(json.dumps(summarize(rows), indent=2))
    else:
        rows = [x for x in read_rows(args.path) if not x.get("skipped")]
        left = [x for x in rows if x["experiment_id"] == args.left]
        right = [x for x in rows if x["experiment_id"] == args.right]
        print(json.dumps(paired_records(left, right, args.metric), indent=2))


if __name__ == "__main__":
    main()
