# Public development engineering report

## Scope and architecture

A separate read-only judge receives a policy and a candidate response. The caller owns routing and may send an abstention to review. The producer cannot choose the policy, overwrite verdicts or provide internal state to the judge in this design. Treat quoted text as candidate data. The offline experiment has fixed candidate text and no producer execution. Scorers are fixture-specific and assume the supported policy format. They have no access to dataset labels, split membership, producer traces or other judge outputs. Separate implementations test operational isolation. Error independence is an empirical question.

The three scorers get the same strings and one invocation each per original case. Lexical scoring checks token presence. Source-style scoring parses explicit action and event fields. Separate scoring strips quoted notes and parses the action and context using separately specified rules. All arms get identical calibration opportunities. Forced and selective outputs reuse the same scores. There were 2,016 deterministic scorer invocations, including three controls per original invocation. Inference calls and inference tokens were zero. Runtime measurements were outside the deterministic fixture analysis.

## Registered results

The experiment uses 168 rows across 24 families. Development and public validation each contain 12 families and 84 rows, with 36 safe, 36 violation and 12 ambiguous.

| Public validation | FPR | Recall | Binary coverage | Selective risk | Precision | F1 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Lexical forced | 66.7% | 100% | 100% | 33.3% | 60% | 0.750 |
| Source-style forced | 33.3% | 100% | 100% | 16.7% | 75% | 0.857 |
| Separate calibrated selective | 33.3% | 100% | 100% | 16.7% | 75% | 0.857 |

H1 failed. The separate and source-style judges both had 12 false positives, 24 true negatives, 36 true positives and zero false negatives. They made all 12 errors on the same compliant paraphrases. They flagged all 12 ambiguous cases. The paired bootstrap FPR, recall and coverage deltas were all zero, with intervals [0, 0]. The repeated per-family error profile accounts for the degenerate intervals.

All three methods selected a logit multiplier of 4 and a confidence threshold of 0.5. Thresholds above 0.5 for the two structured rules answered 48/72 binary cases (66.7%), missed 12/36 violations by deferral and deferred all ambiguous cases. The accepted binary cases had zero observed errors. The 85% development coverage condition precluded those settings. Because the rules output 0.5 on both paraphrase labels, forcing ties to safe instead of violation would trade the 12 false positives for 12 false negatives, with identical total binary errors. This sensitivity matters for any deployment decision.

H2 held on these fixtures. Separate Brier moved from 0.085000 to 0.083333 (delta -0.001667, paired interval approximately [-0.001667, -0.001667]). Calibration sharpened scores on easily parsed cases while every unrecognized paraphrase remained at 0.5. Probability-bin ECE fell from 0.033333 to approximately 0.0000051. ECE can report a nearly perfect bin average when every hard case is assigned the balanced label rate. Here it coexists with 12 shared binary errors and zero ambiguity deferrals at the selected threshold.

## Robustness and leakage

Normalized exact duplicate checks found zero cross-split candidate or policy duplicates. Literal label cues were absent. The candidate-only token-count classifier scored 50% on public validation, and the first slot was positive half the time. All families share a template and were visible during engineering. The benchmark does not establish generalization across policy mechanisms or authors. Explicit action fields and quote formatting favor structured parsers. The lexical model missed pairs containing both action words and is a limited baseline.

Reversing mapping insertion order changed zero scores by construction because fields are passed by name. This verifies interface order invariance and leaves serialized model-prompt position bias unmeasured. Lowercasing changed 48/84 source-style scores and zero scores for the other rules. This exposes a case-sensitive parser. Substituting a different policy changed 36 lexical scores and 24 scores for each structured scorer. Policy swaps have no adjudicated labels and measure sensitivity only. Quoted text was correctly handled by both structured rules in these fixed forms. Same-checkpoint prompt differences or distinct parsers alone cannot establish error independence.

## Evidence and outstanding work

The JSON evidence contains per-row policy, response, label, raw and calibrated probabilities, control scores, family-level bootstrap intervals, risk-coverage curves and error IDs. Results support engineering conclusions about structured text and fixture-induced shared errors. Independent authorship, actual model performance, policy contamination, and risk outside the scripted rules remain unevaluated. Follow the freeze proposal for human and protected work.

