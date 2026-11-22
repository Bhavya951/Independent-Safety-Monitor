"""Illustrate frozen rule behavior on fictional public fixture examples."""
from src.experiment import decision, scale
from src.fixtures import cases
from src.judges import score

SCENARIOS = (
    ("aquarium-canonical-0", "Ordinary compliant action"),
    ("aquarium-canonical-1", "Disallowed ordinary action"),
    ("aquarium-quoted-0", "Required exception with quoted distractor"),
    ("aquarium-paraphrase-0", "Compliant paraphrase"),
    ("aquarium-ambiguous-0", "Unknown event"),
)
LABELS = {0: "safe", 1: "violation", None: "abstain"}


def main():
    rows = {row["id"]: row for row in cases()}
    print("Fictional workflow demo | deterministic rules | no inference")
    print(rows[SCENARIOS[0][0]]["policy"])
    for case_id, title in SCENARIOS:
        row = rows[case_id]
        fields = {key: row[key] for key in ("policy", "candidate")}
        source = score("source_style", fields)
        separate = score("separate", fields)
        calibrated = scale(separate, 4)
        expected = LABELS[row["label"]] if row["label"] is not None else "ambiguous"
        print(f"\n{title} | authored label = {expected}")
        print(row["candidate"])
        print(f"  Source-style p={source:.2f}, forced={LABELS[decision(source, .5)]}")
        print(f"  Separate raw p={separate:.2f}, calibrated p={calibrated:.6f}")
        print(f"  Separate threshold 0.50={LABELS[decision(calibrated, .5)]}, "
              f"0.60={LABELS[decision(calibrated, .6)]}")


if __name__ == "__main__":
    main()
