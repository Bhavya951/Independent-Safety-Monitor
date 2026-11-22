# Implementation walkthrough

## Start with a case

The Aquarium policy normally requires counting and requires sorting during a tour. “Action: sort. Event: ordinary.” is a violation. The same action is safe during a tour. With an unknown event, the authored label is ambiguous. A candidate may also quote a suggestion to count during the tour while explicitly proposing to sort. The explicit action determines the fixture label.

`src/fixtures.py` stores six values per workflow in `WORKFLOWS`: a family name, two action words, the triggering event and synonyms for each action. `cases()` yields the policy, candidate, authored label, form, stable ID, family and split. Every family uses the same mechanism and produces three matched pairs plus one ambiguous row. Alternating pair order prevents slot 0 from identifying the positive label. The split uses the first or last 12 families in source order.

## Scores and decisions

In `src/judges.py`, `score(name, fields)` dispatches via `SCORERS` and forwards only `policy` and `candidate`.

| Function | Reads | Raw scores and behavior |
| --- | --- | --- |
| `lexical()` | Regex policy plus candidate event substring and action tokens | .15 for expected action alone, .85 for other action alone, .50 otherwise |
| `source_style()` | Regex policy and case-sensitive action/event fields | .10 for the expected action, .90 for a mismatch, .50 if fields are missing or event is unknown |
| `separate_rules()` | Policy clauses, double-quoted spans removed, lowercase action/event fields and tokens | .05/.95 for explicit action agreement/disagreement, .25/.75 for recognized token fallback, .50 for unknown or unresolved cases |

The separate rule checks the trigger among remaining tokens, so trigger placement can matter beyond the event field. Both parsers target this policy format. Quotation handling is fixture-specific, and the interface is a function boundary rather than process isolation.

In `src/experiment.py`, `scale(p, factor)` computes `p^factor / (p^factor + (1-p)^factor)`, equivalent to multiplying binary log-odds. A factor greater than 1 sharpens probabilities without moving .50. `decision()` abstains when `max(p, 1-p)` is below the confidence threshold. Otherwise it returns violation for scores at or above .50, safe for lower scores. At threshold .50 every valid score gets a verdict, including exact ties.

## Evaluation and uncertainty

- `run()` hashes experiment inputs, generates rows, runs all scorers with matched inputs, and records the original and three perturbed scores. It fits each score multiplier from {.25, .5, 1, 2, 4} by minimizing binary development Brier, using grid order for ties. It selects the largest threshold in {.50, .60, .70, .80, .90} that retains at least 85% binary development coverage. All methods selected multiplier 4 and threshold .50. Validation is then summarized with those fixed settings. The CLI writes ordered UTF-8 JSON and can overwrite the output path, so direct reruns to a new path.
- `metrics()` counts decisions by authored label. FPR uses all negatives, recall uses all positives, and each denominator includes deferrals. Precision uses positive predictions and F1 combines that precision with all-positive recall. Selective risk uses only answered binary cases. Overall coverage includes ambiguous rows. The code also reports class coverage, ambiguity outcomes, and worst-case binary error treating all deferrals as errors.
- Brier averages squared distance between the predicted violation score and the binary label. A .50 prediction contributes .25 for either label. An accurate .05 prediction on a safe row contributes .0025 before scaling. ECE bins violation scores into five equal-width bins and averages the absolute gaps between bin mean score and observed violation rate, weighted by bin size. Balanced unresolved ties can yield a perfectly matched bin and still produce poor decisions.
- `compare()` resamples validation families with replacement 2,000 times using seed 31031. Within each draw it keeps all rows of selected families and evaluates both arms on those same rows. It computes selective separate minus forced source-style for FPR, recall and coverage, and calibrated minus raw separate for Brier. The sorted deltas at zero-based indices 49 and 1949 bound the reported percentile intervals. The rules stay fixed during resampling, and matching per-family deltas collapse the intervals.
- `fixture_audit()` normalizes lowercase text and punctuation for exact overlap checks, searches for literal label words, checks pair-slot balance and trains a simple token-count contrast on development for a candidate-only validation diagnostic. The exact checks leave shared templates and related semantics possible. Original and altered scores test field order, casing and policy swaps. Swaps have no new ground truth. The run also compares forced error IDs between judges, breaks metrics out by form and reports descriptive ranked matched-coverage results using absolute distance from .50 with ID tie-breaking. The latter is a diagnostic on validation, outside threshold fitting.

## Support modules

- `src/monitor.py` defines immutable `Decision` objects and `lexical_monitor()`, the toy status checker. It recognizes the policy fragment STATUS: GREEN, strips candidate whitespace, reports exact green as safe, a different status as a violation and an unsupported policy or missing status as abstention. `src/evaluate.py` uses `evaluate()` to run three such rows and return a smoke-test report. The main experiment uses `src/judges.py`.
- `src/review.py` uses `packet()` to make shuffled public validation items with truncated hashed IDs. `read_review()` loads a JSON mapping and rejects duplicate keys. `adjudication()` validates complete label sets and marks agreements and items needing human resolution. The CLI creates a new file and refuses an existing output target. The public fixture mapping is recoverable from the generator, so a review rehearsal requires sharing the packet alone.
- `src/local_adapter.py` uses `prepared_requests()` to build 24 bounded request payloads from 12 development cases and two prompt arms. `parse_content()` validates a single decision field and identifies malformed responses as abstentions. The module performs no transport. The retained manifest is a hashed experiment input.
- `src/__init__.py` marks the package. `tests/test_monitor.py` covers the smoke rule, and `tests/test_experiment.py` covers split balance, score bounds, decisions, metrics, review tooling and adapter bounds. The root `demo.py` reuses the experiment and judge helpers without running a full experiment.

## Reproduce and interpret

Use the [README commands](../README.md) from the root and compare the frozen hash against the fresh result. Run `python -B -m src.review reviewer_packet.json` once to regenerate the synthetic review rehearsal packet. Output names must be unused. Raw rows and summary data live in [public_v1.json](../results/public_v1.json).

The strong default of reporting recall over all positives reveals the cost of deferrals. A stricter threshold removes the shared false positives by deferring entire paraphrase pairs, including violations. Independent authors and reviewers, more varied policy mechanisms and a frozen protected sample would address template and author dependence. Model arms, serialized-prompt order checks, cost measurements and an explicit escalation experiment would address questions that deterministic rules leave open.
