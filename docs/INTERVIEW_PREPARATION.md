# Technical interview preparation

## 30-second introduction

I built an offline experiment to test whether a separately implemented monitor could cut false alarms on fictional workflow rules. I compared three deterministic judges with identical inputs, split by policy family and fitted calibration on development. The two structured judges made the same twelve false positives, so the main hypothesis failed. Calibration slightly improved Brier score while leaving the hard cases unresolved.

## Two-minute research explanation

The motivating question was whether separating oversight from the original judging logic could reduce false alarms while keeping useful recall and coverage. I represented review as a narrow function from written policy and candidate text to a violation score. The comparators were a lexical rule, a source-style parser and a separate parser. The experiment invoked each once per unmodified case and reused scores for forced and selective decisions.

The fixture has 24 fictional families. Each contains canonical, paraphrased and quoted pairs plus one ambiguous row. I split whole families and fitted a scalar calibration and confidence cutoff only on the development half. The registered H1 gate required at least a five-point FPR reduction while retaining recall and coverage, keeping selective risk within ten percent and obtaining a paired interval below zero for FPR.

On validation both structured rules flagged the same twelve safe paraphrases. The cutoff of .50 forced ties into violation and gave 100% binary coverage with 16.7% selective risk. Raising the cutoff deferred both safe and violating paraphrases. H2 held by about .001667 Brier because easy predictions became sharper, while difficult ones stayed at .50. Resampling the twelve families in matched pairs yielded degenerate intervals because their error profiles repeated. The experiment establishes fixture behavior. Independent case authorship, human adjudication and protected model testing remain open.

## Technical questions

1. **What is independent about the monitor?** It has a separately implemented scoring rule and a narrow two-string input interface. Its errors can still correlate with the source-style rule because of shared inputs and parsing assumptions.

2. **Where is the producer?** Candidate text is fixed by the generator. A production producer and escalation router are architectural ideas beyond this offline run.

3. **Are these LLM judges?** All three scores come from deterministic Python functions. The separate adapter builds model-request objects offline and executed zero inference.

4. **How is baseline access matched?** Each scorer receives one identical policy and candidate per original row, with three matched control calls. Labels, IDs and split metadata stay in the evaluator.

5. **Why include a lexical baseline?** It tests how far basic token presence goes. It is limited by quoted distractors and synonym substitutions, so it provides a simple floor beside the structured comparator.

6. **How do the structured rules differ?** The source-style judge requires case-sensitive Action and Event fields. The separate parser removes quoted spans, normalizes case and can fall back to token checks.

7. **How were labels created?** They are assigned by construction from the action and event rule. Missing context is ambiguous. Human annotation and agreement remain unmeasured.

8. **Why split by family?** Paired variants share wording and context, so a row split would put related versions in both fitting and evaluation. The family split still shares a generator and was visible to the engineering author.

9. **What constitutes a false positive?** A safe authored case receives a violation decision. The registered FPR divides by all safe binary cases, including any safe cases that were deferred.

10. **What happens to a deferred violation?** It remains in the recall denominator and contributes no true positive. This keeps reduced coverage from silently inflating recall.

11. **How do overall and binary coverage differ?** Overall coverage includes ambiguous rows, binary coverage uses only safe and violation rows. Report ambiguity deferral directly as well.

12. **How is selective risk computed?** Divide answered binary mistakes by answered binary cases. Report coverage and worst-case error alongside it because deferral can hide operational burden.

13. **What is Brier score?** The mean of squared differences between violation probabilities and binary labels. A .50 score costs .25 for either label and more accurate probabilities reduce the loss.

14. **How was calibration fitted?** Each scorer selects a positive logit multiplier from .25, .5, 1, 2 and 4 to minimize binary development Brier. The selected multiplier is applied unchanged on validation.

15. **How was the decision threshold selected?** Use the largest registered confidence cutoff with at least 85% binary development coverage. Every scorer chose .50, whose inclusive boundary forces a verdict even at an exact tie.

16. **Why did H1 fail?** FPR stayed at 33.3%, the paired FPR interval was [0, 0], and selective risk was 16.7%, above the 10% ceiling. Recall and coverage both met their gates at 100%.

17. **Why was H2 only narrowly supported?** Brier improved by about .001667 on the fixture. The gain came from sharpening easy cases. All paraphrase ties remained at .50 and the hard decisions stayed the same.

18. **How can ECE be nearly zero alongside twelve false positives?** The .50 bin is balanced with equal numbers of safe and violation labels, so its average score matches its event rate. Forcing every tie to violation still misclassifies every safe member.

19. **Would flipping the tie convention solve H1?** For the frozen paraphrases it would exchange 12 false positives for 12 false negatives on validation. That would sacrifice 33.3 recall points, exceeding the allowed loss.

20. **What changes at threshold .60?** Both halves of the paraphrase pairs defer. Binary coverage and recall each fall to 66.7%. All ambiguous cases defer and answered binary errors are zero on this fixture.

21. **Why bootstrap families?** Rows within a family share the same policy and are intentionally paired. Sampling entire families retains dependence. Using the same sampled families for both scorers keeps their difference paired.

22. **How do you interpret the zero-width intervals?** The family resamples repeat the same delta profile, so the empirical percentile endpoints coincide. There are 12 validation clusters from a shared template and no population sample.

23. **What does the leakage audit show?** There were zero normalized exact cross-split matches or literal label cues. The token-count diagnostic reached 50% and first-slot order was balanced. Semantic overlap and shared templates remain.

24. **What did robustness controls test?** Field insertion order checks named access, lowercasing exposes source-style sensitivity, and policy swapping tests response to the rule text without new labels. Fixed quoted text tests the supported formatting.

25. **What is matched-coverage ranking?** Sort binary cases by distance from .50 and answer the same number as the separate selective arm. This is a descriptive validation diagnostic, with stable ID tie-breaking.

26. **How do you explain AI assistance?** Say that AI assisted engineering and release documentation. Point to the registration, frozen evidence, reproducible commands and tests for verifiable claims. Distinguish development assistance from inference during the study.

27. **How would you validate the scientific claim next?** Use independently authored families and blinded labels, adjudicate disagreements, then lock the protocol and analysis before a separately authorized protected run. Compare same-checkpoint prompt arms and distinct-model arms at matched information and budgets.

28. **What would you add for deployment?** Measure escalation workload, confidence stability under shift, hard-case errors, costs, latency and monitor–producer error overlap. Specify unsupported-input handling and evaluate the complete routing policy.

29. **How can someone reproduce the released result?** Run the README experiment with a new output path on Python 3.15.2 and compare SHA-256. The original artifact stores code, test and registration hashes, and Git attributes preserve their bytes.

## Practice with artifacts

Rehearse with the [live demo](LIVE_DEMO.md), trace the scorer and metric paths using the [implementation walkthrough](IMPLEMENTATION_EXPLAINED.md), and prepare for related-work questions with the [paper guide](RESEARCH_PAPERS_EXPLAINED.md).
