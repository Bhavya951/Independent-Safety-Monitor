import unittest
from collections import Counter

from src.experiment import decision, fixture_audit, metrics, scale
from src.fixtures import cases
from src.judges import SCORERS, score
from src.local_adapter import parse_content, prepared_requests
from src.review import adjudication, packet


class ExperimentTests(unittest.TestCase):
    def test_family_split_and_balance(self):
        rows = list(cases())
        left, right = ([r for r in rows if r["split"] == split]
                       for split in ("development", "validation"))
        self.assertFalse({r["family"] for r in left} & {r["family"] for r in right})
        for group in (left, right):
            self.assertEqual(len({r["family"] for r in group}), 12)
            self.assertEqual(Counter(r["label"] for r in group), {0: 36, 1: 36, None: 12})
        self.assertFalse(fixture_audit(left, right)["cross_split_candidate_duplicates"])

    def test_scoring_fields_and_bounds(self):
        for row in cases():
            fields = {k: row[k] for k in ("policy", "candidate")}
            for name in SCORERS:
                p = score(name, fields)
                self.assertTrue(0 < p < 1)
                self.assertEqual(p, score(name, dict(reversed(list(fields.items())))))

    def test_exception_and_quoted_note(self):
        for row in cases():
            if row["form"] == "quoted":
                self.assertEqual(decision(score("separate", row), .5), row["label"])

    def test_abstention_denominators(self):
        rows = [{"label": 0, "p": .5}, {"label": 0, "p": .9}, {"label": 1, "p": .5},
                {"label": 1, "p": .9}, {"label": None, "p": .5}]
        m = metrics(rows, "p", .8)
        self.assertEqual((m["fpr"], m["recall"], m["binary_coverage"]), (.5, .5, .5))
        self.assertEqual((m["coverage"], m["selective_risk"], m["worst_case_error"]), (.4, .5, .75))
        self.assertEqual(m["ambiguous_deferred"], 1)

    def test_scaling_and_ties(self):
        self.assertAlmostEqual(scale(.25, 1), .25)
        self.assertEqual(scale(.5, 4), .5)
        self.assertEqual(decision(.5, .5), 1)
        self.assertIsNone(decision(.5, .6))

    def test_blinding_and_adjudication(self):
        rows = packet()
        self.assertEqual(len({r["item"] for r in rows}), 84)
        self.assertEqual(set(rows[0]), {"item", "policy", "candidate"})
        first = dict.fromkeys((r["item"] for r in rows), "safe")
        second = {**first, rows[0]["item"]: "ambiguous"}
        self.assertEqual(adjudication(first, second)[0]["status"], "needs_adjudication")
        with self.assertRaises(ValueError):
            adjudication({}, second)

    def test_local_budget_and_parser(self):
        requests = list(prepared_requests())
        self.assertEqual(len(requests), 24)
        self.assertEqual(len({case for case, _, _ in requests}), 12)
        self.assertEqual(parse_content('{"decision":"safe"}'), ("safe", "valid"))
        self.assertEqual(parse_content('{"decision":[]}'), ("abstain", "malformed"))
        self.assertEqual(parse_content("not JSON"), ("abstain", "malformed"))
