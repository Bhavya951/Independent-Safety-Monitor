# Research papers explained

Bibliographic details and the study summaries below were checked against the primary records.

## Constitutional AI: Harmlessness from AI Feedback

Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, and Jared Kaplan (2022). [Primary paper](https://arxiv.org/abs/2212.08073)

How can explicit principles guide assistant training while reducing reliance on human harmlessness labels? The supervised stage uses principle-guided critiques and revisions of sampled replies. In the reinforcement stage, AI comparisons train a preference model whose reward is used to optimize the assistant. Human evaluation indicated gains in harmlessness with less evasiveness in their setup. Results depend on the principles, evaluators and prompt distribution. Our monitor likewise receives written rules, but scores fixed toy responses during evaluation and performs no training.

### Interview questions

1. **What is the constitution?** Written principles used to guide revisions and preference judgments.
2. **What is RLAIF?** Reinforcement learning from AI feedback, using AI preference labels to fit a reward model.
3. **Why are there two stages?** The first learns from revised examples. The second optimizes against preferences over sampled replies.
4. **Where does human judgment enter?** People specify the principles and evaluate behavior. The harmlessness training signal is generated using AI feedback.
5. **Is our judge a reproduction of Constitutional AI?** Our judge is a rule parser applied to fixed responses. The paper changes model behavior through training.

## Training language models to follow instructions with human feedback

Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe (2022). [Primary paper](https://arxiv.org/abs/2203.02155)

The authors study whether language models can follow user intent better with human feedback. They fine-tune GPT-3 on demonstrations from labelers, fit a reward model to ranked outputs, and optimize a policy with reinforcement learning. In their human evaluation, 1.3B InstructGPT was preferred over 175B GPT-3 on the study prompt distribution. The models still made mistakes, and preferences depend on whose instructions and judgments are sampled. Our project also depends on a source of labels, here fixed by synthetic construction, and runs no optimizer over a language model.

### Interview questions

1. **What are the three main stages?** Supervised fine-tuning, preference reward modeling and RL policy optimization.
2. **How do demonstrations differ from rankings?** Demonstrations supply desired outputs. Rankings compare alternatives the model produced.
3. **What does the size comparison show?** On the sampled prompts, human preference could favor a much smaller instruction-tuned model.
4. **What limits transfer of the result?** Prompt populations, annotator criteria, deployment conditions and persistent model errors.
5. **How are our labels different?** They follow a generated action/event rubric. No annotator rankings or reward model are involved.

## Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica (2023). [Primary paper](https://arxiv.org/abs/2306.05685)

The paper examines whether model judges can scale open-ended assistant evaluation. MT-Bench uses multi-turn questions and Chatbot Arena collects human comparisons. Strong judges like GPT-4 showed over 80% agreement in reported human-preference comparisons. Position, verbosity and self-enhancement biases and reasoning errors limit reliability. Our study borrows the comparator idea but uses pointwise rubric scores for one fixed candidate at a time. Mapping insertion order checks the Python interface only.

### Interview questions

1. **What is measured by agreement?** How often judge preferences match the human decisions under the comparison protocol.
2. **What is position bias?** A tendency to favor an answer based on presentation order. Swap answers to probe it.
3. **Why can verbosity matter?** A judge may prefer length even when extra text does not improve an answer.
4. **What is self-enhancement bias?** A judge may favor outputs from its own model or model family.
5. **Does our order control test pairwise position bias?** It tests named Python field access. A true position check would vary serialized prompts or candidate ordering in model calls.

## Selective Classification for Deep Neural Networks

Yonatan Geifman and Ran El-Yaniv (2017). [Primary paper](https://arxiv.org/abs/1705.08500)

The authors ask how a trained classifier can meet a target error rate by rejecting uncertain examples. They use confidence-ranked selective prediction and a held-out procedure to control risk with high probability under their assumptions. CIFAR and ImageNet experiments show that lower accepted-case error is achievable at reduced coverage. Guarantees rely on statistical assumptions and a suitable sample. Our evaluation chooses a threshold by development coverage and reports empirical risk on clustered fixture rows.

### Interview questions

1. **What is a reject option?** A classifier may decline to predict and defer the decision.
2. **What is selective risk?** The fraction of answered examples that are wrong.
3. **What is coverage?** The fraction of all examples that receive a prediction.
4. **Why is zero observed risk insufficient?** It reflects only accepted examples in a finite sample. The rejected examples may include many important positives.
5. **Why does the paper's guarantee not transfer here?** We use a coverage-based grid and clustered templates, with no risk-control guarantee calculated.

## On Calibration of Modern Neural Networks

Chuan Guo, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger (2017). [Primary paper](https://arxiv.org/abs/1706.04599)

The paper examines whether model confidence reflects empirical correctness. It evaluates calibration methods on image and document classification and finds that many modern architectures are poorly calibrated. Temperature scaling adjusts logits with one parameter fitted on held-out data and worked well on many benchmarks. Calibration is distribution-dependent, and binned measures hide within-bin errors. We borrow scalar logit scaling but select a binary multiplier with a fixed Brier grid and evaluate violation-frequency bins rather than top-label confidence bins.

### Interview questions

1. **What does a temperature do?** It divides logits before softmax. In the binary case our factor is the reciprocal of a temperature.
2. **Does positive scaling change the forced label?** It preserves score order and the .50 boundary, with possible finite-precision caveats in general.
3. **How does our fit differ?** The paper fits temperature using held-out negative log likelihood. We select a multiplier by binary Brier loss on development.
4. **Can ECE be low while error remains high?** Yes. A balanced bin predicted at .50 can be calibrated in aggregate while its forced decisions make errors.
5. **Why fit on development only?** It avoids choosing the factor from the same validation labels used to assess the fitted score.
