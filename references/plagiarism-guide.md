# Plagiarism & Similarity Guide

## How Similarity Detection Works

### The Mechanism

Plagiarism detectors (Turnitin Similarity, iThenticate, Crossref) are **completely separate** from AI detectors. They work by:

1. **Normalize** the document (encoding, whitespace, punctuation)
2. **Tokenize** into words
3. **Fingerprint** overlapping k-grams (sequences of 5-10 words) into hashes
4. **Winnow** the hash set to representative fingerprints
5. **Query** a massive index of web pages, journals, and prior submissions
6. **Reconstruct** matches into contiguous spans
7. **Report** a similarity percentage and source list

The key insight: **similarity detection is string matching, not semantic analysis.** It catches copied phrases, not borrowed ideas.

### What It Catches
- Verbatim copying
- Close paraphrase with retained structure and vocabulary
- Self-plagiarism (if prior work is indexed)
- Translated plagiarism (less reliably)

### What It Does NOT Catch
- Genuine paraphrase with different structure
- Original synthesis of multiple sources
- Ideas without attribution (that's intellectual dishonesty, but not string-matchable)

---

## How to Actually Fix High Similarity

### Step 1: Identify the Flagged Spans

Most plagiarism reports highlight exact phrases. Before fixing anything, categorize each match:

| Match Type | Action |
|-----------|--------|
| **Direct quote with citation** | Legitimate — no fix needed. Ensure quotes marks and citation are present |
| **Common phrase / technical definition** | Often a false positive. Add citation if needed, or rephrase your framing around it |
| **Paraphrased source, too close** | Must rewrite — see technique below |
| **Self-plagiarism** | Must rewrite or cite your own prior work |
| **Accidental match** | Check — may be coincidence on a common phrase |

### Step 2: The Honest Rewriting Technique

For content that's too similar to a source:

1. **Read the source carefully** — understand the concept fully
2. **Close the source document** — do not look at it while writing
3. **Wait 5 minutes** — let the exact phrasing fade
4. **Write from memory** — explain the concept as if teaching someone
5. **Use completely different sentence structures:**
   - If the source used a long compound sentence, use two short ones
   - If the source listed items, embed them in narrative prose
   - If the source used passive voice, use active
   - If the source started with the conclusion, start with the evidence
6. **Verify accuracy** — reopen the source and check your facts
7. **Add your own framing** — why does this matter for YOUR argument?
8. **Cite the source** — even perfectly paraphrased ideas need attribution

### Step 3: What NEVER Works

| Bad Technique | Why It Fails |
|--------------|-------------|
| **Synonym spinning** | Keeps the same structure; sophisticated detectors catch it; reads worse |
| **Reordering words** | k-gram overlap remains; structure unchanged |
| **Adding filler words** | Increases word count but k-grams still match |
| **Changing tense** | Minor change; most k-grams still match |
| **Back-translation** | Produces unnatural phrasing; academic misconduct if undisclosed |
| **Invisible characters** | Normalized by preprocessing; bad faith |

### Step 4: For Research Papers Specifically

#### Citing Correctly
```
WRONG: The protein folding problem has been studied extensively.
(This matches dozens of papers)

RIGHT: Chen et al. (2023) classified three subtypes of protein 
misfolding in their analysis of 1,200 patient samples.
(Specific, cited, and structurally unique)
```

#### The "So What?" Test
After every paraphrased passage, add your own analytical sentence:
```
SOURCE: "Machine learning models achieve 94% accuracy on benchmark X."

YOUR PARAPHRASE + ANALYSIS:
"On benchmark X, ML models reach 94% accuracy (Smith, 2024). 
However, this benchmark uses cleaned data that rarely matches 
real-world noise levels."
```

Adding your own analysis — your opinion, your comparison, your question — is the single best way to reduce similarity while adding value.

---

## Common Plagiarism Scenarios

### Scenario 1: Literature Review
**Problem:** Summarizing multiple papers inevitably produces similar phrasing.

**Fix:**
- Use a thematic structure instead of paper-by-paper summaries
- Compare and contrast studies: "While A found X, B found Y"
- Add your own synthesis: "Three common limitations emerge across these studies..."
- Focus on what matters for YOUR research question

### Scenario 2: Methods Section
**Problem:** Standard methods use standard descriptions.

**Fix:**
- Cite the original method paper
- Describe only your specific implementation details
- "We followed the protocol of Zhang (2022) with two modifications..."
- Unique parameter values naturally differentiate your description

### Scenario 3: Definitions and Background
**Problem:** Domain terms have standard definitions.

**Fix:**
- Use the briefest possible definition with citation
- Frame it in terms of your specific application
- "For this analysis, we define X as [definition] (following Author, Year)"

### Scenario 4: Previously Published Pilot Data
**Problem:** Self-plagiarism when building on your own prior work.

**Fix:**
- Explicitly cite your prior work
- Clearly state what is new vs. previously published
- Rewrite the shared content; do not copy-paste from your own paper
- Many journals have specific policies — check before submitting

---

## Similarity Score Targets

| Context | Typical Acceptable Range | Notes |
|---------|------------------------|-------|
| Undergraduate essay | < 15-20% | Varies by institution |
| Masters thesis | < 10-15% | Check university policy |
| PhD dissertation | < 10% | Most flagged content should be properly quoted |
| Journal article | < 15% (varies) | References/bibliography usually excluded |
| Conference paper | < 20% | May overlap with extended journal version |

**Important:** These are guidelines, not laws. A 25% similarity score where every match is a properly cited direct quote is fine. A 5% score with uncited close paraphrase is not.

---

## The Bottom Line

Plagiarism cannot be "fixed" by a tool. It can only be fixed by:
1. Understanding the source material deeply
2. Writing in your own words and structure
3. Citing every source, even when paraphrased
4. Adding your own analysis, opinions, and connections

No synonym spinner, paraphraser, or AI tool can substitute for actually engaging with the material.



---

## 5. Mathematical Equations, Formulas, & Algorithm Plagiarism

One of the most common ways research papers get flagged in Turnitin and iThenticate is through **mathematical equations, derivations, theorem statements, and pseudocode algorithms**.

### Why Equations Get Flagged by Similarity Checkers
Similarity engines (Turnitin, iThenticate, Crossref) don't understand math semantically. They convert LaTeX source code into text tokens and compare token $k$-grams:
1. **Identical Variable Conventions:** Copying standard variable names, indices, and subscripts ($x_i, y_i, \mathbf{W}_q, \mathbf{W}_k, \lambda$).
2. **Identical Surrounding Scaffolding:** Scanners flag the text leading into and out of formulas ("where $N$ denotes the total number of samples and $\sigma$ represents the standard deviation").
3. **Element-wise vs. Vectorized Clones:** Standard summation expansions copied character-for-character from famous papers.
4. **Pseudocode Algorithm Lines:** Generic variable names (`input: X`, `for i = 1 to N do`, `return Y`).

---

### How to Fix Equation & Math Plagiarism (100% Mathematical Equivalence)

#### Technique 1: Systematic Variable Notation Shift
Without changing mathematical meaning, adapt variable naming to fit your paper's unique notation namespace:

| Standard / Copied Notation | Mathematically Equivalent Humanized Notation | Rationale |
|---|---|---|
| $\mathcal{L}_{\text{total}} = \lambda_1 \mathcal{L}_{\text{rec}} + \lambda_2 \mathcal{L}_{\text{reg}}$ | $\mathcal{J}(\theta) = \alpha \cdot \mathcal{E}_{\text{recon}} + \beta \cdot \mathcal{R}_{\text{norm}}(\theta)$ | Changes the objective notation from generic $\mathcal{L}$ to explicit objective $\mathcal{J}$ parameterized by $\theta$. |
| $\text{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}$ | $\sigma\left(d_k^{-1/2} \mathbf{S}\right)\mathbf{V}, \quad \text{where } \mathbf{S} = \mathbf{Q}\mathbf{K}^\top$ | Introduces intermediate affinity tensor $\mathbf{S}$ and negative exponent notation $d_k^{-1/2}$, breaking the verbatim character sequence. |
| $\text{Loss} = -\sum_{i=1}^C y_i \log(\hat{y}_i)$ | $\mathcal{L}_{\text{CE}}(y, p) = -\mathbf{y}^\top \log \mathbf{p} = -\sum_{c \in \mathcal{C}} \mathbb{I}(y = c) \log p_c$ | Shifts from scalar index sum to vector dot product or indicator function notation. |
| $f(x) = \frac{1}{1 + e^{-x}}$ | $\sigma(z) = \left(1 + \exp(-z)\right)^{-1} = \frac{\exp(z)}{\exp(z) + 1}$ | Expresses logistic activation with inverted power or normalized exponent form. |

#### Technique 2: Vectorized vs. Component-Wise Representation
- If a source paper presents an operation in component-wise scalar loops:
  $$\mu = \frac{1}{m} \sum_{i=1}^m x_i, \quad \sigma^2 = \frac{1}{m} \sum_{i=1}^m (x_i - \mu)^2$$
- Rewrite in compact matrix/vector notation:
  $$\boldsymbol{\mu} = m^{-1} \mathbf{X}^\top \mathbf{1}_m, \quad \boldsymbol{\Sigma} = m^{-1}(\mathbf{X} - \mathbf{1}_m \boldsymbol{\mu}^\top)^\top (\mathbf{X} - \mathbf{1}_m \boldsymbol{\mu}^\top)$$
- Or conversely, expand an opaque matrix equation into clear, explicit component sums tailored to your domain application.

#### Technique 3: Dissociate Surrounding Scaffolding
Never use standard boilerplate to introduce equations:
- ❌ **Flagged:** *"The loss function is defined as shown in Equation (1), where $N$ denotes the batch size, $y_i$ is the ground truth, and $\hat{y}_i$ represents the predicted probability:"*
- ✅ **Clean:** *"We penalize prediction divergence using weighted cross-entropy across all $N$ batch elements (Equation 1):"*
- ❌ **Flagged:** *"where $\epsilon$ is a small constant added for numerical stability."*
- ✅ **Clean:** *"To guard against division by zero in floating-point operations, we add a floor offset $\epsilon = 10^{-8}$."*

#### Technique 4: Pseudocode & Algorithm Refactoring
1. **Reorder Independent Declarations:** Swap order of independent variable initializations, tensor allocations, or parameter instantiations.
2. **Rename Function Signatures:** Instead of generic `ForwardPass(x)` or `TrainEpoch()`, use descriptive domain procedures: `EvaluateGradients(batch, weights)`, `PropagateAttention(nodes, edges)`.
3. **Change Control Constructs:** Replace procedural loops with vectorized functional operations:
   - Instead of:
     ```text
     for i = 1 to B do
         loss_i = ComputeLoss(y_i, p_i)
     total_loss = sum(loss) / B
     ```
   - Write:
     ```text
     BatchLoss = Mean(Map(ComputeLoss, Zip(Y_batch, Predictions)))
     ```
   - Or present as structured mathematical steps rather than code blocks.

---

### Step-by-Step Equation & Plagiarism Audit Checklist

Before submitting any manuscript, thesis, or technical report:
- [ ] **Exact Match Check:** Did you copy any 2+ line equation directly from another paper's LaTeX source? If yes, adjust variable notation and decomposition.
- [ ] **Scaffolding Check:** Re-read every "where $x$ is..." explanation. Ensure the prose has your unique sentence rhythm and vocabulary.
- [ ] **Derivation Steps:** When showing derivations or proofs, do not copy intermediate steps verbatim. Insert explanatory commentary explaining *why* a substitution is valid in your context.
- [ ] **Constants and Hyperparameters:** Cite the source when adopting hyperparameters from another paper: *"Following Smith et al. [12], we set temperature $\tau = 0.07$ and learning rate $\eta = 3 \times 10^{-4}$."* (Transparent citation turns potential similarity into scholarly rigor).
