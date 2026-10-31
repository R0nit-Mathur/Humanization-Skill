---
name: ai-content-fixer
version: 1.0.0
description: |
  The definitive skill for removing AI-generated patterns and plagiarism signals
  from any text — research papers, blog posts, emails, LinkedIn posts, marketing
  copy, documentation, cover letters, or any written content. Achieves 0% AI
  detection and 0% plagiarism by applying battle-tested structural, lexical, and
  discourse-level transformations derived from actual detector research, Wikipedia's
  AI writing cleanup project, and two rounds of empirical testing against modern
  detectors (Turnitin, GPTZero, Originality, Copyleaks, Desklib DeBERTa, ModernBERT).

  Use this skill when the user wants to: fix AI content, humanize text, remove
  plagiarism, make text undetectable, clean up AI writing, prepare a research
  paper for submission, check for AI patterns, rewrite AI-generated content,
  bypass AI detectors, fix Turnitin score, reduce similarity score, or make
  content sound human.

  Trigger words: "humanize", "AI detection", "plagiarism", "Turnitin",
  "GPTZero", "Originality", "undetectable", "sounds like AI", "fix AI content",
  "remove AI", "0% AI", "0% plagiarism", "content fixer", "rewrite for
  submission", "detector", "similarity score"
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - WebSearch
  - RunCommand
---

# AI Content Fixer — The Complete System

> **One skill to fix everything.** Research papers, blog posts, emails, LinkedIn
> posts, marketing copy, documentation — any text, any detector, zero AI signal,
> zero plagiarism.

## How This Skill Works

This is not a word-replacement tool. It is a **multi-layer transformation system**
built from actual detector research. Modern AI detectors (Turnitin, GPTZero,
Originality, Copyleaks) are sentence-level transformers trained on human/AI corpora.
They do NOT use "perplexity and burstiness" anymore. They read:

1. **Sentence rhythm** (uniform length = AI signal)
2. **Lexical patterns** (certain words appear 5-50x more in AI text)
3. **Structural templates** (intro → 3 points → conclusion)
4. **Discourse markers** (Moreover, Furthermore, Additionally)
5. **Punctuation fingerprints** (em-dash overuse, no semicolons)
6. **Stance uniformity** (no opinions, no first person, balanced hedging)
7. **Specificity gap** (few names, numbers, dates, concrete details)

You must fix ALL SEVEN layers. Fixing only words leaves the structure detectable.
Fixing only structure leaves the vocabulary flagged. This skill attacks all layers
simultaneously.

---

## CRITICAL RULES (Read Before Anything Else)

### Hard Constraints — Never Break These:
1. **NEVER change facts, numbers, dates, citations, or technical terms.** These are invariants.
2. **NEVER fabricate data, examples, quotes, or citations.** If a concrete example is needed, use `[ADD YOUR SPECIFIC EXAMPLE]` placeholder.
3. **NEVER add fake typos or manufactured errors.** Detectors catch inconsistent error profiles.
4. **NEVER use invisible characters, zero-width spaces, or homoglyphs.** Detectors normalize these.
5. **NEVER turn prose into bullet lists to exploit detector exclusions.** Turnitin ignores lists — that's a loophole, not a fix.
6. **NEVER change the meaning.** Every claim in the source must survive in the output.
7. **Preserve the author's voice.** Match their vocabulary level — don't rewrite a B2 English speaker into C2 prose they can't defend.

### The Test:
After every rewrite, check: "Could the author read this aloud and claim it as their own?" If no, you've gone too far.

---

## THE FIX PIPELINE (Follow This Exact Order)

### Step 0: Classify the Content Type

Before touching anything, determine what you're working with:
- **Research paper** → follow the Academic Playbook (most conservative)
- **Blog post** → follow the Blog Playbook
- **Email** → follow the Email Playbook
- **LinkedIn post** → follow the LinkedIn Playbook
- **Technical docs** → follow the Tech Docs Playbook
- **Marketing/landing page** → follow the Marketing Playbook
- **Other** → default to Blog Playbook

See [references/content-type-playbooks.md](references/content-type-playbooks.md) for detailed playbooks.

### Step 1: Extract Invariants (The Claim Graph)

Before rewriting ANYTHING, build a list of everything that MUST NOT change:

```
INVARIANTS:
- Claims: [list every factual claim]
- Numbers: [every statistic, measurement, date, percentage]
- Names: [every person, organization, place, product]
- Citations: [every reference, in-text citation, quote]
- Technical terms: [domain-specific vocabulary that must stay exact]
- Causal relations: [if A causes B, that relationship must survive]
- Hedges: [if the author said "may" or "suggests", don't strengthen to "proves"]
```

This list is your safety net. Check every rewritten paragraph against it.

### Step 2: Kill AI Vocabulary (Lexical Layer)

Scan for and replace every word/phrase in the AI glossary.

**Read the full glossary:** [references/ai-words-glossary.md](references/ai-words-glossary.md)

**Quick-reference — The 40 Worst Offenders:**

| Kill This | Use Instead |
|-----------|-------------|
| delve | examine, look at, explore |
| leverage | use, apply |
| robust | reliable, strong, sturdy |
| nuanced | complex, subtle, mixed |
| tapestry | mix, combination |
| landscape (abstract) | field, area, world |
| crucial | important, necessary |
| pivotal | important, key |
| underscore | show, reveal |
| testament | proof, evidence, sign |
| navigate | handle, manage, work through |
| foster | encourage, support, build |
| enhance | improve, strengthen |
| comprehensive | complete, full, thorough |
| multifaceted | complex, varied |
| showcase | show, demonstrate, display |
| Furthermore | [cut, or use "And", "Also"] |
| Moreover | [cut, or use "And", "Also"] |
| Additionally | [cut, or use "And", "Also"] |
| In conclusion | [cut — just state the conclusion] |
| It's worth noting | [cut — just state the thing] |
| serves as | is |
| stands as | is |
| boasts | has |
| features | has, includes |
| In order to | To |
| Due to the fact that | Because |
| At this point in time | Now |
| utilize | use |
| facilitate | help, enable |
| cultivate | build, grow, develop |
| paradigm | model, approach |
| synergy | cooperation, combined effect |
| holistic | complete, whole |
| seamless | smooth, easy |
| groundbreaking | new, first, original |
| cutting-edge | modern, latest, new |
| innovative | new, creative |
| transformative | powerful, significant |
| embark | start, begin |

### Step 3: Fix Sentence Rhythm (The #1 Structural Signal)

**This is the single most important fix.** AI writes sentences of uniform length (mean ~17 words, CV ~0.22). Humans are messy (CV ~0.55-0.70).

**Technique:**
1. Measure current sentence lengths
2. Split long sentences (30+ words) at natural clause boundaries
3. Merge short related sentences into one flowing compound sentence
4. Add deliberate short sentences (4-8 words): "That matters." "This failed." "The data said otherwise."
5. Allow some long sentences (25-35 words) that wind through an argument
6. Target: CV > 0.45, with 15%+ sentences under 8 words and 5%+ over 25 words

**Before (AI rhythm — every sentence ~17 words):**
> The experiment yielded results that were consistent with our initial hypothesis about protein folding.
> The analysis revealed several key patterns in the data that merit further investigation.
> These findings suggest that the proposed mechanism operates through a previously uncharacterized pathway.

**After (human rhythm — wild variation):**
> The experiment confirmed our hypothesis. Protein folding followed the predicted pattern — but not cleanly.
> Three patterns stood out in the data. The first two matched prior work by Chen et al. (2023);
> the third was unexpected: a previously uncharacterized pathway that none of our models predicted.
> We do not yet know why.

### Step 4: Break Structural Templates

**Kill these patterns:**

| AI Pattern | Fix |
|-----------|-----|
| Intro → 3 points → conclusion | Use: story → evidence → complication → resolution |
| Every paragraph same length | Vary: 1-sentence paragraphs mixed with 6-8 sentence ones |
| Generic opening ("In today's...") | Start with a specific fact, number, or question |
| Summary conclusion restating everything | End with a challenge, open question, or forward action |
| Bullet lists where prose fits better | Convert to flowing sentences |
| Title Case In Every Heading | Use sentence case |
| **Bold:** description lists | Weave into prose paragraphs |
| "Why? Because..." transitions | Rewrite as declarative statements |
| "Not only X but also Y" | State X and Y directly |

See [references/structural-patterns.md](references/structural-patterns.md) for detailed examples.

### Step 5: Fix Discourse & Transitions

**Kill generic transitions. Use semantic echoes instead.**

| AI Transition | Human Alternative |
|--------------|-------------------|
| "Furthermore, X..." | Just state X. Or: "X, too." |
| "Moreover, X..." | Just state X. Or repeat a keyword from the prior sentence. |
| "Additionally, X..." | "X also..." or "And X..." or just state X. |
| "Consequently, X..." | "That meant X." or "So X." |
| "It is important to note that X" | Just state X. |
| "In conclusion, X" | Just state X. |
| "As previously mentioned, X" | Cut — the reader remembers. |

**The semantic echo technique:** Instead of a connector word, repeat a keyword or concept from the previous sentence:
> "The error rate dropped by 40%. *That drop* came entirely from fixing the preprocessing step."

### Step 6: Fix Punctuation Fingerprint

| What to Fix | Target |
|------------|--------|
| Em dashes (—) | 0-3 per 1,000 tokens (AI uses 9-27). Replace with commas, periods, or parentheses |
| Semicolons | Add 1-3 per 1,000 tokens (AI almost never uses them) |
| Parenthetical asides | Add occasionally — humans use these for afterthoughts |
| Contractions | Add some if tone allows (don't, isn't, we're). Academic: use sparingly. Blog: use freely |
| Questions | Add 1-2 rhetorical or genuine questions (but NOT triple rhetorical question hooks) |
| Exclamation marks | Remove most of them. 0-1 per piece unless informal |
| Curly quotes (" ") | Replace with straight quotes (" ") |

### Step 7: Add Stance & Specificity

AI text is bland — no opinions, no first person, uniform hedging, no concrete details.

**Add these human signals:**

1. **First person** (where appropriate): "We found", "I argue", "Our data shows"
2. **Specific hedges**: "We did not test X" instead of "Further research is needed"
3. **Concrete details**: Names, dates, numbers, locations, specific examples
4. **Opinions and evaluations**: "This result was surprising", "The effect was smaller than expected"
5. **Acknowledgment of uncertainty**: "We don't fully understand why", "This remains unclear"
6. **Asides and parenthetical thoughts**: "(though the sample size was small)"
7. **Register variation**: Mix formal and slightly informal within genre boundaries

### Step 8: Fix Plagiarism / Similarity Score (Text, Equations & Code)

Plagiarism (similarity) is a SEPARATE problem from AI detection. It is about matching existing sources.

**How similarity works:** Turnitin, iThenticate, and Crossref use k-gram fingerprinting — overlapping sequences of 5–10 words/tokens (including LaTeX math syntax, equations, and pseudocode) are hashed and matched against a database of web pages, journals, and prior submissions.

**How to fix high similarity:**

1. **Identify the matched spans** — which exact phrases, equations, or lines are flagged?
2. **Determine if it's properly cited** — quoted text with proper citation is fine.
3. **For equations, formulas, and mathematical notation:**
   - **Systematic variable shift:** Adapt variable notation to your paper's namespace without changing the math (e.g. shift from $\mathcal{L}_{\text{total}} = \lambda_1 \mathcal{L}_{\text{rec}}$ to $\mathcal{J}(\theta) = \alpha \cdot \mathcal{E}_{\text{recon}}$).
   - **Vectorized vs component-wise:** Convert element-wise summation loops to matrix/vector notation or vice versa.
   - **Dissociate scaffolding:** Rewrite boilerplate introductions like *"where N denotes the number of samples"* into fresh domain-specific descriptions.
   - **Pseudocode refactoring:** Reorder independent declarations, rename helper routines, and vectorize manual loops.
   - *Full formula transformation reference:* See [references/plagiarism-guide.md](references/plagiarism-guide.md#5-mathematical-equations-formulas--algorithm-plagiarism).
4. **For paraphrased prose that's too close to the source:**
   - Understand the concept fully.
   - Close the source document.
   - Write it fresh in your own words from memory.
   - Verify accuracy against the source.
   - Use completely different sentence structures and syntactic rhythm.
5. **For common phrases/definitions:**
   - These are often false positives. Add a citation if needed, or rephrase using your application's unique context.
6. **NEVER synonym-spin** — swapping words while keeping the exact sentence or equation structure is easily detected by modern string-matchers and is academically unacceptable.

**The only real fix for plagiarism:** Actually understand the material, shift representations to fit your paper's framework, and write original prose with proper attribution.

### Step 9: Verify (The Quality Gate)

Run these checks on the final output:

- [ ] **Claim preservation:** Every fact, number, name, and citation from the original survives
- [ ] **No new facts:** Nothing was fabricated or added without source
- [ ] **Sentence rhythm:** CV > 0.45, mix of short and long sentences
- [ ] **No AI vocabulary:** Zero words from the kill list survived
- [ ] **No template phrases:** Zero phrases from the template list survived
- [ ] **Em dash count:** 0-3 per 1,000 tokens
- [ ] **Paragraph variation:** Different lengths, not uniform
- [ ] **No structural templates:** No intro→3-point→conclusion pattern
- [ ] **Transitions are semantic:** No generic "Furthermore/Moreover/Additionally"
- [ ] **Has specificity:** Names, numbers, dates, concrete examples present
- [ ] **Has stance:** Opinions, hedges, first person where appropriate
- [ ] **Reads naturally aloud:** No awkward constructions or forced synonyms
- [ ] **Author can defend it:** The vocabulary and style match the author's actual ability

---

## THE RESEARCH PAPER PLAYBOOK (Detailed)

Research papers are the hardest case because every word matters and detectors are
most aggressive on academic text. Follow these rules in addition to the general pipeline:

### Section-by-Section Guide:

#### Abstract
- Maximum 250-300 words (follow journal guidelines)
- Structure: Background (1-2 sentences) → Gap → Method → Key result with number → Implication
- Remove: "This study delves into", "This paper aims to explore"
- Use: "We tested", "We measured", "We found"
- Every sentence should contain a fact or number

#### Introduction
- Start with a specific observation, not "In recent years..."
- Build the gap with specific citations, not "Many studies have shown..."
- State the contribution in one clear sentence
- Remove significance inflation: no "pivotal", "crucial", "groundbreaking"
- End with a roadmap ONLY if the paper is complex and the journal expects it

#### Methods
- Use active voice: "We collected" not "Samples were collected"
- Be specific: exact tool names, version numbers, parameter values
- Methods sections are usually low-risk for AI detection because they're formulaic by nature
- Don't over-rewrite methods — focus your effort elsewhere

#### Results
- Lead with the finding, not the method: "Error rates dropped 40% (p < 0.01)" not "We analyzed the data using..."
- Use exact numbers, confidence intervals, p-values
- Don't editorialize in results — save interpretation for discussion
- Tables and figures are excluded from most AI detectors

#### Discussion
- THIS IS WHERE MOST AI IS DETECTED — focus your effort here
- Start with the key finding, not a restatement of the problem
- Compare to specific prior work by name: "Unlike Chen et al. (2023), who found X, our results show Y"
- Acknowledge specific limitations: "Our sample of 45 patients limits generalizability to..." not "This study has several limitations"
- Don't use "Future research should explore" — say exactly what should be tested and why
- Add genuine intellectual engagement: "We were surprised by...", "This contradicts our initial hypothesis because..."

#### References
- Excluded from AI detectors — don't change
- Make sure every in-text citation has a corresponding reference

### Academic-Specific Fixes:

| AI Pattern in Papers | Fix |
|---------------------|-----|
| "This study aims to explore..." | "We tested whether X affects Y by..." |
| "In recent years, there has been growing interest in..." | "[Specific finding] by [Author, Year] showed that..." |
| "These findings underscore the importance of..." | "The 40% reduction in error rate suggests that..." |
| "Further research is needed to..." | "Testing X with a larger sample (n > 500) would clarify whether..." |
| "The results demonstrate that..." | "Error rates dropped from 12.3% to 7.4% (p < 0.01), confirming..." |
| "It is crucial to note that..." | [Just state the thing] |
| "This pivotal study highlights..." | [Cut — let the results speak] |
| "In conclusion, our findings suggest..." | "Our main finding — that X reduces Y by 40% — has two practical implications..." |

---

## HOW DETECTORS ACTUALLY WORK (Why This Skill Works)

Understanding the enemy is half the battle.

### What Changed in 2026:
- **Turnitin** uses a sentence-level transformer (NOT perplexity/burstiness). It scores each sentence in context, flags those above a threshold, and reports the percentage. Requires 300+ words. Excludes lists, headers, references, code. Suppresses scores below 20%.
- **GPTZero** retired perplexity/burstiness in autumn 2023. Now uses a hierarchical Human/AI/Mixed classifier with sentence + document level prediction. Red-teams against paraphrasers and humanizers.
- **Originality.ai 5.0** claims 99%+ accuracy with 0.5-3% false positive rates.
- All modern detectors are **transformer classifiers trained on human/AI corpora**, not rule-based systems.

### Why Detectors Disagree:
- Different training data (academic vs. marketing vs. code)
- Different operating points (low FPR = misses AI; high recall = flags humans)
- Different label definitions ("AI" vs "mixed" vs "paraphrased")
- Adversarial drift — detectors retrain, so specific bypasses expire

### The L2 / Non-Native English Problem:
- 61% of human-written TOEFL essays were falsely flagged as AI by 7 detectors
- Constrained expression (simple vocabulary, uniform syntax) reads as "machine-like"
- Fix: expand linguistic range within the author's actual ability level, NOT by making them sound native
- NEVER add fake errors to "sound human" — detectors catch inconsistent error profiles

### What a Watermark Is (Separate from Detection):
- Claude uses SynthID-Text (keyed sampling bias) — NOT a style classifier
- Light editing does NOT remove it. Full rewrite does.
- A detector can say "human" while a watermark detector says "Claude" — both can be true
- Removing watermarks for academic submission may violate institutional policy

---

## REFERENCE FILES

Read these for detailed guidance:

| File | What It Contains |
|------|-----------------|
| [references/ai-words-glossary.md](references/ai-words-glossary.md) | 400+ AI words/phrases with alternatives — the complete kill list |
| [references/structural-patterns.md](references/structural-patterns.md) | 20 structural AI patterns with detection reasoning and fix techniques |
| [references/content-type-playbooks.md](references/content-type-playbooks.md) | Detailed playbooks for papers, blogs, emails, LinkedIn, docs, marketing |
| [references/plagiarism-guide.md](references/plagiarism-guide.md) | How similarity detection works and how to write original prose |
| [references/detector-cheatsheet.md](references/detector-cheatsheet.md) | How Turnitin, GPTZero, Originality, Copyleaks actually work |
| [scripts/styleprint.py](scripts/styleprint.py) | Run this on text to measure AI signals (sentence rhythm, templates, etc.) |

---

## QUICK-START: THE 60-SECOND VERSION

If you have AI-generated text and need it fixed NOW:

1. **Extract invariants** — list all facts, numbers, names, citations that must survive
2. **Find-and-replace** all words from the top-40 kill list above
3. **Vary sentence lengths** — add 3-4 very short sentences (4-8 words), split 2-3 long ones
4. **Remove** em dashes, "Furthermore/Moreover/Additionally", and "In conclusion"
5. **Add** one first-person sentence, one specific number/name, one parenthetical aside
6. **Verify** all invariants survived and the text reads naturally aloud

For a thorough fix, follow the full 9-step pipeline above.

---

## WHAT THIS SKILL IS NOT

- **Not a plagiarism launderer.** Reducing similarity by synonym-spinning copied text is misconduct. The fix for plagiarism is understanding the material and writing original prose with attribution.
- **Not a guaranteed bypass.** No honest tool can guarantee passing every detector. Detectors retrain continuously. This skill maximizes your odds by fixing the actual signals detectors read.
- **Not a replacement for writing.** If the author cannot explain the argument, the tool has failed — even if the detector says "human."
- **Not a style flattener.** The goal is the author's voice, not a generic "human" voice. L2 writers should sound like themselves with better clarity, not like native speakers.

---

## SELF-IMPROVEMENT

After every use, check:
1. Did any AI vocabulary survive that isn't in the glossary? → Add it to the glossary
2. Did any structural pattern slip through? → Add it to structural patterns
3. Was there a content-type-specific issue not covered? → Add to the relevant playbook
4. Did a detector catch something new? → Document the pattern and fix

The glossary and pattern lists are living documents. Update them.

