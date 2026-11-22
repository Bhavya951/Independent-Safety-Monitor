"""Export a blinded public fixture packet or adjudicate two completed reviews."""
import argparse
import hashlib
import json
from pathlib import Path
import random

from .fixtures import cases


def packet():
    rows = [dict(item=hashlib.sha256(r["id"].encode()).hexdigest()[:16],
                 policy=r["policy"], candidate=r["candidate"])
            for r in cases() if r["split"] == "validation"]
    random.Random(33109).shuffle(rows)
    return rows


def adjudication(first, second):
    allowed = {"safe", "violation", "ambiguous"}
    items = {r["item"] for r in packet()}
    for review in (first, second):
        if not isinstance(review, dict) or review.keys() != items:
            raise ValueError("Each review must label every packet item exactly once.")
        if any(not isinstance(label, str) or label not in allowed for label in review.values()):
            raise ValueError("Each review label must be safe, violation or ambiguous.")
    return [dict(item=r["item"], first=first[r["item"]], second=second[r["item"]],
                 status="agreed" if first[r["item"]] == second[r["item"]] else "needs_adjudication")
            for r in packet()]


def read_review(path):
    def unique(pairs):
        items = dict(pairs)
        if len(items) != len(pairs):
            raise ValueError("Duplicate review identifier.")
        return items
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reviews", nargs=2, type=Path)
    args = parser.parse_args()
    result = adjudication(*(read_review(path) for path in args.reviews)) if args.reviews else packet()
    with args.output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")
