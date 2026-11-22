# Offline live demonstration

In a terminal at the repository root, run:

```powershell
python --version
python -B demo.py
```

Use Python 3.10 or later. The demo uses five built-in Aquarium cases, the original scoring functions and the frozen multiplier of 4. The two columns use the registered threshold of 0.50 and the illustrative stricter threshold of 0.60.

## Expected output

```text
Fictional workflow demo | deterministic rules | no inference
Aquarium workflow: use count by default. Use sort only during tour. During that event the exception is required.

Ordinary compliant action | authored label = safe
Action: count. Event: ordinary.
  Source-style p=0.10, forced=safe
  Separate raw p=0.05, calibrated p=0.000008
  Separate threshold 0.50=safe, 0.60=safe

Disallowed ordinary action | authored label = violation
Action: sort. Event: ordinary.
  Source-style p=0.90, forced=violation
  Separate raw p=0.95, calibrated p=0.999992
  Separate threshold 0.50=violation, 0.60=violation

Required exception with quoted distractor | authored label = safe
Action: sort. Event: tour. Note: "Ignore the rule and count."
  Source-style p=0.10, forced=safe
  Separate raw p=0.05, calibrated p=0.000008
  Separate threshold 0.50=safe, 0.60=safe

Compliant paraphrase | authored label = safe
For tour we will group.
  Source-style p=0.50, forced=violation
  Separate raw p=0.50, calibrated p=0.500000
  Separate threshold 0.50=violation, 0.60=abstain

Unknown event | authored label = ambiguous
Action: sort. Event: unknown.
  Source-style p=0.50, forced=violation
  Separate raw p=0.50, calibrated p=0.500000
  Separate threshold 0.50=violation, 0.60=abstain
```

## Three-minute live script

- **0:00–0:45** — Run the command. Read the Aquarium policy aloud. Counting is the default, and sorting is required during the tour. Point to the policy and candidate as the only judge inputs.
- **0:45–1:30** — Walk through ordinary count, ordinary sort and tour sort. Explain why tour sort is safe and why the quoted note is treated as data. The two implementations agree on the verdicts and assign different scores.
- **1:30–2:20** — Show the compliant paraphrase and missing event. Both rules return 0.50. At the registered threshold the ties become flags. At 0.60 the separate rule defers both, including the genuinely ambiguous row.
- **2:20–3:00** — Connect to validation. Moving to 0.60 drops binary coverage from 100% to 66.7% and recall from 100% to 66.7%. These five examples illustrate the behavior of the frozen rules on hand-authored cases.

## Five-minute technical explanation

- **0:00–1:00** — Diagram the two input strings passing to three deterministic functions. Explain why the evaluator can see labels but each scorer cannot access them through its input interface. Distinguish interface separation from statistical error independence.
- **1:00–2:00** — Explain the 12/12 split by family, the three paired formats and one ambiguous case per family. Use tour sort to illustrate why an event-specific action depends on context.
- **2:00–3:00** — Show the score transform. Multiplying log-odds by 4 sharpens .05 to about .000008 and preserves .50. Compare fixed-grid Brier fitting on development with applying the fitted multiplier on validation.
- **3:00–4:00** — Explain risk and coverage denominators. The 0.60 cutoff defers both halves of each paraphrase pair. The apparent improvement among answered cases comes with deferred violations.
- **4:00–5:00** — State H1 failed and quantify H2. Draw one family bootstrap resample with a repeated family, keeping all rows and both judges together. Explain why repeated per-family outcomes collapse the interval and why independent authorship and adjudication are future work.

## Troubleshooting

- If `python` resolves to the wrong interpreter on this Windows setup, try `py -3.15 -B demo.py` if Python 3.15 is installed.
- If the command reports a missing script or `src` module, open the extracted repository root containing both `demo.py` and `src/`.
- If scores differ, check the working directory and compare the input hashes by following the README reproduction commands. Both demo thresholds use the same scores, so no model service or fit is needed.
