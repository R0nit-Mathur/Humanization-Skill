# Detector Cheatsheet — How They Actually Work (October 2026)

> **Key insight:** Every detector described here is a probabilistic classifier with
> error rates. None of them "prove" anything. A detector score is evidence for a
> human decision, not a verdict.

---

## 1. Turnitin AI Writing Detection

**Mechanism:** Sentence-level transformer trained on in-house academic data.

**What it actually does:**
- Assigns a score to each sentence *in context*
- Sentences above a threshold are labeled "AI"
- Reports the percentage of evaluated sentences above threshold
- Requires ≥300 words of prose
- Excludes: lists, headers, references, code, quoted text
- Suppresses scores below 20% (to reduce false positives)

**What it does NOT do:**
- Does NOT use hand-coded "perplexity" or "burstiness" features
- Does NOT determine academic misconduct (their own docs say this)
- Does NOT evaluate text under 300 words

**Claims:**
- <1% document-level false positive rate
- Validated on 700,000 pre-ChatGPT papers
- Claims to detect paraphraser/bypasser-modified text

**Exploitable weaknesses (for understanding, not for cheating):**
- Lists and headers are excluded → but turning prose into lists is a loophole, not a fix
- Text under 300 words is not scored → but artificially shortening text defeats the purpose
- The 20% display floor means scores between 1-19% are silently suppressed

**Source:** [Turnitin FAQ](https://guides.turnitin.com/hc/en-us/articles/28477544839821)

---

## 2. GPTZero

**Mechanism:** Deep learning, hierarchical multi-task architecture.

**What it actually does:**
- Level 0: Human / AI / Mixed classification
- Level 1: Pure AI / Polished / AI-Paraphrased subclassification
- Predicts at both document and sentence level in one forward pass

**What it does NOT do:**
- Does NOT use perplexity or burstiness anymore (retired autumn 2023)
- The "perplexity" and "burstiness" explanations on their site are legacy

**Red-teaming (what they test against):**
- Paraphrasing prompts
- Dipper-style paraphrasers
- Black-box humanizer tools
- White-box token substitution attacks
- Translation chains

**Source:** [GPTZero Technical Report, arXiv:2602.13042](https://arxiv.org/abs/2602.13042)

---

## 3. Originality.ai

**Mechanism:** Supervised transformer classifier.

**Claims (v5.0, October 2026):**
- 99%+ accuracy
- False positive rates: 0.5-3% depending on model and operating point
- "AI Allowance" thresholds (0/5/15/25/40%) — an admission that binary is the wrong question

**Notable:** Reports false-positive rates by model version, which is unusually transparent.

**Source:** [Originality.ai Accuracy Page](https://originality.ai/blog/ai-accuracy)

---

## 4. Copyleaks

**Mechanism:** Sentence-level classifier with document aggregation.

**What it does:**
- Highlights sentences classified as AI
- Reports document-level percentage
- Claims multi-language support

---

## 5. Winston AI

**Mechanism:** Supervised classifier.
- Reports a percentage AI score
- Less publicly documented than competitors

---

## 6. ZeroGPT

**Mechanism:** Proprietary classifier.
- Reports percentage human/AI
- Less documentation available

---

## 7. GPTInf (Aggregator)

**Mechanism:** Not a detector itself — runs text through 8 third-party detectors and shows the spread.

**Why this matters:** GPTInf's design is accidentally the most honest in the category: it shows you that detectors disagree, rather than presenting one score as truth.

**Source:** [GPTInf Help Center](https://help.gptinf.com/hc/en-us/articles/48076651326609)

---

## 8. Open-Source Detectors (for research/testing)

| Model | Training Data | Architecture | Strengths | Weaknesses |
|-------|--------------|-------------|-----------|------------|
| Desklib DeBERTa v1.01 | RAID (6M generations) | DeBERTa-v3-large | Strong against paraphrase; adversarial-trained | May over-flag L2 text |
| ModernBERT AI detector | rasbt/human-vs-ai-50k | ModernBERT | Holds up on held-out data | Smaller training set |
| OpenAI RoBERTa | GPT-2 era data | RoBERTa-base | Historical baseline | Outdated; modern AI bypasses it trivially |
| HC3 RoBERTa | HC3 ChatGPT data | RoBERTa | In-domain for Q&A | Narrow training; paraphrase-vulnerable |

---

## Why Detectors Disagree

1. **Different labels.** One detector's "AI" is another's "mixed"
2. **Different training data.** Academic vs marketing vs code
3. **Different operating points.** Low FPR = misses AI; high recall = flags humans
4. **Adversarial drift.** RAID benchmark found detectors "easily fooled" by attacks, sampling changes, and unseen models
5. **Base-rate problem.** Even 99% accuracy produces many false positives when AI prevalence is low
6. **Construct problem.** "AI-generated" isn't well-defined. A human-edited AI draft, an AI-polished human draft, and a translation are all boundary cases

---

## The L2 False Positive Problem

**The most important fairness finding in detection:**

Liang et al. (2023) evaluated 7 detectors on 91 human-written TOEFL essays:
- **61.22% average false positive rate** (flagged as AI)
- **97.80%** flagged by at least one detector
- **19.78%** unanimously flagged by all 7 detectors
- Native 8th-grade essays: only **5.19%** FPR

**Why:** Constrained expression (simpler vocabulary, more uniform syntax) statistically resembles AI output.

**Fix:** "Enhance word choices to sound more like a native speaker" dropped FPR from 61.22% to 11.77%. The reverse (simplifying native text) raised FPR from 5.19% to 56.65%.

**Implication:** For L2 writers, "humanization" is often de-biasing, not deception. But naive "sound native" rewrites erase the writer's voice. The right fix: expand range within the author's zone of proximal development.

---

## Watermarks (Separate from Detection)

### SynthID-Text (Claude/Google)
- Modifies sampling procedure, not the model
- Biases token choices using a secret key
- Detection: compute mean g-value of tokens under the key
- Light editing does NOT remove it; full rewrite does
- Weaker on short text and low-entropy text (formulas, facts with one correct phrasing)
- Global, no opt-out (Claude, August 2026)

### textGrain (OpenAI)
- Partitions vocabulary into blocks; uses Gumbel optimal transport
- ~95% detection at 400 tokens, ~80% at 200, ~66% after 10% synonym substitution
- EU ChatGPT/Codex only; API opt-in
- 200-token threshold matches EU exemption

### Critical Fact
**A classifier can say "human" while a watermark detector says "Claude."** Both can be true. They measure different things. Treat them as separate channels.

---

## What No Detector Can Do

- **Prove authorship.** Detection ≠ attribution.
- **Determine misconduct.** Turnitin's own docs say this explicitly.
- **Be 100% accurate.** All have false positives and false negatives.
- **Stay accurate forever.** Models change, generators change, the boundary moves.
- **Handle boundary cases.** Human-edited AI text, AI-polished human text, and translations are fundamentally ambiguous.

---

## The FTC Warning

In 2025, the FTC ordered an AI detection company (Workado) to stop claiming 98% accuracy when independent testing found 53%. Unsupported accuracy claims about AI detection are a legal risk.

**Source:** [FTC Press Release](https://www.ftc.gov/news-events/news/press-releases/2025/04/ftc-order-requires-workado-back-artificial-intelligence-detection-claims)

