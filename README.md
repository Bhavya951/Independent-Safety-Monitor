# Independent Safety Monitor

Can a separately implemented reviewer reduce false alarms while still catching explicit rule violations? This project tests that question on fictional workflow responses. The registered false-positive hypothesis failed. Calibration produced a small improvement in Brier score on the public fixture.

The source-style judge and separate monitor are deterministic rules, not independently deployed language models. The experiment used fixed candidate text and zero model calls. Separation means the monitor has its own scoring implementation and receives only policy text and candidate text. The evaluator holds labels and split metadata and joins them to predictions for analysis. Shared failure modes remain possible.

## Fixture and comparators

The generator builds 24 workflow families around a shared default action and mandatory event exception. Each family contributes three safe/violation pairs (canonical fields, paraphrased actions, and structured fields with a quoted distractor) plus one ambiguous row. The first 12 families are development and the last 12 are public validation. Each split has 36 safe, 36 violation and 12 ambiguous rows. Labels are authored by construction.

The lexical baseline uses token presence. The source-style rule looks for explicit action and event fields. The separate rule strips quoted strings, normalizes case, and uses its own parsing and token checks. Each receives identical inputs and one invocation per original case, plus three robustness invocations. Each has the same calibration opportunity. Forced and selective outputs reuse scores. The frozen experiment recorded 2,016 deterministic calls.

## Registered results

| Public validation | FPR | Recall | Binary coverage | Selective risk |
| --- | ---: | ---: | ---: | ---: |
| Lexical forced | 66.7% | 100% | 100% | 33.3% |
| Source-style forced | 33.3% | 100% | 100% | 16.7% |
| Separate calibrated selective | 33.3% | 100% | 100% | 16.7% |

- **H1 was unsupported.** The separate selective rule needed a reduction of at least 5 percentage points in FPR, at most a 5-point recall loss, at least 85% binary coverage, at most 10% selective risk, and a paired 95% FPR delta interval entirely below zero. FPR, recall and binary coverage deltas were each 0 points (95% intervals [0, 0]). Both judges shared the same 12 false positives on compliant paraphrases, and selective risk exceeded 10%.
- **H2 held on this fixture.** Development-fitted scalar calibration reduced validation Brier from 0.085000 to 0.083333. The calibrated-minus-raw delta was approximately −0.001667 (paired 95% interval [−0.001667, −0.001667] at this precision). The transform sharpened easy scores and left 0.5 ties fixed. Five-bin ECE fell from 0.033333 to about 0.0000051, while the shared errors persisted.
- **Abstention had a cost.** The selected confidence threshold was 0.5, which flags ties and deferred none of the 12 ambiguous cases. At 0.6 the separate rule deferred all ambiguous cases and reached zero observed accepted-case errors, but binary coverage fell to 48/72 (66.7%) and recall fell to 24/36 (66.7%).

FPR divides false alarms by all safe binary rows. Recall divides detected violations by all violation rows. Both denominators include deferrals. Binary coverage is the fraction of binary rows answered. Overall coverage also counts ambiguous rows in its denominator. Selective risk is the error rate among answered binary rows. Brier is the mean squared probability error, and ECE compares average predicted violation probability with observed violation frequency within bins. Both use all binary rows before abstention.

## Checks and scope

Normalized exact cross-split duplicate checks and literal label-cue checks found zero hits. The candidate-only shortcut scored 50%, and matched pair order was balanced. Field mapping order changed zero scores because the interface extracts inputs by name. Lowercasing changed 48 source-style validation scores and zero separate or lexical scores. Policy swaps changed scores for all methods and test sensitivity without assigning new labels. Both structured rules handled the fixture's quoted distractors.

Shared templates, author-visible validation families, hand-assigned labels and just 12 validation clusters limit inference. The degenerate intervals reflect repeated family outcomes. The study provides fixture-level evidence about rule behavior. Independent authorship and adjudication, frozen protected evaluation and actual model performance remain pending. Future work should vary policy mechanisms and authors, measure reviewer agreement, pre-register a protected evaluation and compare same-checkpoint prompting with distinct-model arms at matched inputs and budgets.

## Reproduce offline

Run from the repository root with Python 3.10+ and the standard library. Windows PowerShell commands below use the available Python interpreter. The frozen run used Python 3.15.2. No package installation is required.

```powershell
python -B -m unittest discover -s tests -v
python -B -m src.evaluate
python -B demo.py
python -B -m src.experiment --output results/reproduced.json
Get-FileHash results/public_v1.json,results/reproduced.json -Algorithm SHA256
```

The expected SHA-256 on the reference runtime is `36d89f06e036df7c0161cc1b89914a30136ceab465242bc59c5288a110846af9` for both files. Other runtimes can differ in recorded version or floating-point serialization. The experiment regenerates fixtures in code and records raw rows, controls, source hashes and statistics. Git attributes preserve byte-level provenance for hashed inputs and evidence.

## Repository guide

- `src/` contains the fixture generator, judges, experiment and offline support code. `tests/` contains the original regression suite.
- [Registration](research/development_registration.md), [engineering report](research/report.md) and [frozen result](results/public_v1.json).
- [Implementation walkthrough](docs/IMPLEMENTATION_EXPLAINED.md), [live demo](docs/LIVE_DEMO.md), [interview preparation](docs/INTERVIEW_PREPARATION.md) and [manual publish checklist](GITHUB_PUBLISH_CHECKLIST.md).
- [Research papers explained](docs/RESEARCH_PAPERS_EXPLAINED.md) covers the original work on Constitutional AI, InstructGPT, LLM judges, selective classification and calibration, with links to all five primary records.

## Development disclosure

The project used AI assistance in engineering and documentation, including this release preparation. The evidence comes from executing deterministic code against synthetic fixtures. The retained offline adapter and feasibility manifest describe a pending experiment and contain no completed inference results.
