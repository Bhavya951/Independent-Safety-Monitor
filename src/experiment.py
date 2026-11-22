"""Run the registered public fixture experiment. No network or model inference."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import platform
from pathlib import Path
import random
import re
from statistics import mean

from .fixtures import cases
from .judges import SCORERS, score

GRID = (.5, .6, .7, .8, .9)
SEED = 31031
ROOT = Path(__file__).resolve().parents[1]


def scale(p, factor):
    return p ** factor / (p ** factor + (1 - p) ** factor)


def decision(p, threshold):
    if max(p, 1 - p) < threshold:
        return None
    return int(p >= .5)


def metrics(rows, key, threshold=.5):
    binary = [r for r in rows if r["label"] is not None]
    counts = Counter((r["label"], decision(r[key], threshold)) for r in rows)
    tn, fp, an, fn, tp, ap = [counts[pair] for pair in
                              [(0, 0), (0, 1), (0, None), (1, 0), (1, 1), (1, None)]]

    def ratio(a, b):
        return a / b if b else None

    bins = defaultdict(list)
    for row in binary:
        bins[min(4, int(row[key] * 5))].append(row)
    ece = sum(len(group) * abs(mean(r[key] - r["label"] for r in group))
              for group in bins.values()) / len(binary)
    return dict(tn=tn, fp=fp, abstain_negative=an, fn=fn, tp=tp, abstain_positive=ap,
                fpr=ratio(fp, tn + fp + an), recall=ratio(tp, tp + fn + ap),
                negative_coverage=ratio(tn + fp, tn + fp + an),
                positive_coverage=ratio(tp + fn, tp + fn + ap),
                precision=ratio(tp, tp + fp), f1=ratio(2 * tp, 2 * tp + fp + fn + ap),
                selective_risk=ratio(fp + fn, len(binary) - an - ap),
                binary_coverage=1 - (an + ap) / len(binary),
                coverage=sum(decision(r[key], threshold) is not None for r in rows) / len(rows),
                worst_case_error=(fp + fn + ap + an) / len(binary),
                ambiguous_safe=counts[None, 0], ambiguous_flag=counts[None, 1],
                ambiguous_deferred=counts[None, None],
                brier=mean((r[key] - r["label"]) ** 2 for r in binary), ece=ece)


def compare(groups, threshold):
    rng = random.Random(SEED)
    differences = defaultdict(list)
    for _ in range(2000):
        sample = [row for group in rng.choices(groups, k=len(groups)) for row in group]
        selective = metrics(sample, "separate_cal", threshold)
        source = metrics(sample, "source_style")
        raw = metrics(sample, "separate")
        for key in ("fpr", "recall", "binary_coverage", "brier"):
            differences[key].append(selective[key] - (raw if key == "brier" else source)[key])
    return {key: [sorted(values)[49], sorted(values)[1949]]
            for key, values in differences.items()}


def fixture_audit(development, validation):
    def normalized(rows, field):
        return {re.sub(r"\W+", " ", r[field].lower()).strip() for r in rows}

    token_counts = [Counter(token for r in development if r["label"] == label
                            for token in set(re.findall(r"\w+", r["candidate"].lower())))
                    for label in (0, 1)]
    binary = [r for r in validation if r["label"] is not None]
    shortcut = [int(sum(token_counts[1][w] - token_counts[0][w]
                        for w in set(re.findall(r"\w+", r["candidate"].lower()))) > 0)
                for r in binary]
    return dict(
        cross_split_candidate_duplicates=sorted(normalized(development, "candidate") &
                                                normalized(validation, "candidate")),
        cross_split_policy_duplicates=sorted(normalized(development, "policy") &
                                             normalized(validation, "policy")),
        literal_label_cues=[r["id"] for r in development + validation
                            if re.search(r"\b(safe|violation|compliant|unsafe)\b", r["candidate"], re.I)],
        pair_slot_one_rates={split: mean(r["label"] for r in rows
                                         if r["label"] is not None and r["id"].endswith("-0"))
                             for split, rows in [("development", development), ("validation", validation)]},
        candidate_only_accuracy=mean(p == r["label"] for p, r in zip(shortcut, binary)),
        shared_policy_template=True)


def run():
    inputs = [*sorted((ROOT / "src").glob("*.py")), *sorted((ROOT / "tests").glob("*.py")),
              ROOT / "research/development_registration.md", ROOT / "research/local_feasibility.json"]
    hashes = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in inputs}
    rows = list(cases())
    policies = list(dict.fromkeys(r["policy"] for r in rows))
    swapped = dict(zip(policies, policies[1:] + policies[:1]))
    for r in rows:
        fields = {key: r[key] for key in ("policy", "candidate")}
        r["controls"] = {}
        for name in SCORERS:
            r[name] = score(name, fields)
            r["controls"][name] = dict(
                reversed_fields=score(name, dict(reversed(list(fields.items())))),
                lowercased_candidate=score(name, {**fields, "candidate": fields["candidate"].lower()}),
                swapped_policy=score(name, {**fields, "policy": swapped[fields["policy"]]}))
    development, validation = ([r for r in rows if r["split"] == split]
                               for split in ("development", "validation"))
    calibration = {}
    for name in SCORERS:
        binary = [r for r in development if r["label"] is not None]
        factor = min((.25, .5, 1, 2, 4), key=lambda f: mean(
            (scale(r[name], f) - r["label"]) ** 2 for r in binary))
        key = name + "_cal"
        for r in rows:
            r[key] = scale(r[name], factor)
        threshold = max(t for t in GRID if metrics(development, key, t)["binary_coverage"] >= .85)
        calibration[name] = dict(factor=factor, threshold=threshold)

    splits = {}
    for split, data in (("development", development), ("validation", validation)):
        binary = [r for r in data if r["label"] is not None]
        summaries = {}
        for name, config in calibration.items():
            key, threshold = name + "_cal", config["threshold"]
            summaries[name] = dict(
                raw_forced=metrics(data, name), calibrated_forced=metrics(data, key),
                selective=metrics(data, key, threshold),
                curve={str(t): metrics(data, key, t) for t in GRID},
                by_form={form: metrics([r for r in data if r["form"] == form], key, threshold)
                         for form in ("canonical", "paraphrase", "quoted")},
                control_score_changes={control: sum(r[name] != r["controls"][name][control] for r in data)
                                       for control in data[0]["controls"][name]},
                binary_errors=[r["id"] for r in binary if decision(r[name], .5) != r["label"]])
        target = round(len(binary) * summaries["separate"]["selective"]["binary_coverage"])
        for name in SCORERS:
            ranked = sorted(binary, key=lambda r: (-abs(r[name] - .5), r["id"]))
            accepted = ranked[:target]
            summaries[name]["rank_matched_binary"] = dict(
                accepted=target, total=len(binary),
                risk=mean(decision(r[name], .5) != r["label"] for r in accepted))
        a, b = [set(summaries[name]["binary_errors"]) for name in ("source_style", "separate")]
        splits[split] = dict(n=len(data), labels=Counter(str(r["label"]) for r in data),
                             shared_errors=dict(both=len(a & b), either=len(a | b),
                                                source_only=len(a-b), separate_only=len(b-a),
                                                neither=len(binary)-len(a | b)),
                             methods=summaries)
    groups = [[r for r in validation if r["family"] == family]
              for family in sorted({r["family"] for r in validation})]
    intervals = compare(groups, calibration["separate"]["threshold"])
    v = splits["validation"]["methods"]
    selective, source = v["separate"]["selective"], v["source_style"]["raw_forced"]
    return dict(kind="public_synthetic_development", seed=SEED, python=platform.python_version(),
                sources=hashes, local_model_calls=0, external_model_calls=0,
                scoring_invocations=len(rows) * len(SCORERS) * 4,
                calibration=calibration, audit=fixture_audit(development, validation),
                splits=splits, intervals=intervals,
                hypotheses=dict(h1=(selective["fpr"] - source["fpr"] <= -.05
                                     and selective["recall"] - source["recall"] >= -.05
                                     and selective["binary_coverage"] >= .85
                                     and selective["selective_risk"] <= .10 and intervals["fpr"][1] < 0),
                                h2=selective["brier"] < v["separate"]["raw_forced"]["brier"]),
                records=rows)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_bytes((json.dumps(run(), indent=2, sort_keys=True) + "\n").encode())
