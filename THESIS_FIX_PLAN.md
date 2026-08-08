# THESIS FIX PLAN — Systematic Revision

**Author:** Mohd Zamin Quadri
**Submission deadline:** April 30, 2026
**Total issues catalogued:** 80
**Estimated total revision time:** 4-6 hours

---

# PART 1 — Prioritized Fix Plan (4 Phases)

## Phase A: CRITICAL (must fix before submission) — 90 min

**Goal:** Eliminate factual errors, numerical inconsistencies, and overclaims that any reviewer will catch.

| # | Issue | Severity | Where | Time |
|---|---|---|---|---|
| 1 | Table 3.1 caption: "training set" → fix | CRITICAL | `03_methodology.tex` L22 | 2 min |
| 6 | "T2-T8 non-zero dropout" excludes T3, T4 (dropout=0) | CRITICAL | `05_results.tex` opening of 5.1 | 3 min |
| 9 | `pos ∈ R^(N×3×2)` notation — clarify start/end/midpoint | CRITICAL | `03_methodology.tex` Table 3.2 + text | 5 min |
| 10 | AUROC text vs Figure 5.10 vs Appendix mismatch (0.7548 vs 0.7538) | CRITICAL | `05_results.tex` + figure caption | 5 min |
| 11 | T11 "1.2% R²" → relative drop is ~2.0% | CRITICAL | `05_results.tex` Section 5.9 | 3 min |
| 13 | "If and only if backbone frozen" too strong | CRITICAL | `06_discussion.tex` RQ5 | 3 min |
| 14 | Conformal "guarantee" wording under node dependence | CRITICAL | `05_results.tex` 5.3, `06_discussion.tex` 6.5 | 5 min |
| 15 | Conclusion "none expensive" / "all model-agnostic" overclaim | CRITICAL | `07_conclusion.tex` | 5 min |
| 16 | T9 "genuine traffic-flow variability" overclaim (Fig 5.14) | CRITICAL | `05_results.tex` Fig 5.14 caption | 5 min |
| 26 | `G=(V,E,X,E)` — E used twice | CRITICAL | `02_background.tex` L13 | 2 min |
| 31 | Remove "Equation (2.4)'s reliability counterpart" | CRITICAL | `03_methodology.tex` L110 | 2 min |
| 70 | RQ5 "if and only if" remove | CRITICAL | `06_discussion.tex` 6.7 | 2 min |
| 8 | Quadrature √ formula — verify PDF rendering | CRITICAL | check final PDF | 5 min |

**Phase A subtotal: ~50 min for fixes + 40 min for compile/proof**

---

## Phase B: METHODOLOGICAL DEFENSIBILITY — 90 min

**Goal:** Soften overclaims, add caveats, clarify methodology.

| # | Issue | Severity | Where |
|---|---|---|---|
| 2 | Batch count: 160-180 vs 200 reconcile | HIGH | `04_experiments.tex` 4.1 |
| 3 | First-20-batches selection bias | HIGH | `04_experiments.tex` 4.1 |
| 4 | T8 selected by test R² → reword as exploratory | HIGH | `04_experiments.tex` 4.2 |
| 5 | T1-T6 vs T7-T8 split caveat | HIGH | `05_results.tex` 5.1 |
| 7 | Deep Ensemble seed 42 (R²=0.640) vs T8 (R²=0.5957) — explain | HIGH | `05_results.tex` 5.6 |
| 12 | Q̂ > 0 gate — add justification | HIGH | `04_experiments.tex` 4.5 |
| 17-25 | Various methodological clarifications | HIGH | Various |
| 60 | T9 "directly demonstrates" → "consistent with" | HIGH | `05_results.tex` 5.7 |
| 61 | T10-v2 vs T11 — verify identical lr | HIGH | `05_results.tex` 5.9 |
| 63 | Section 6.1 "differ only in fine-tuning" — only T10-v2 vs T11 | HIGH | `06_discussion.tex` 6.1 |
| 65-68 | Soften causal claims throughout | HIGH | `06_discussion.tex` |

**Phase B subtotal: ~90 min**

---

## Phase C: NOTATION + EQUATION POLISH — 45 min

| # | Issue | Where |
|---|---|---|
| 27 | Directed neighbourhood incoming/outgoing | `02_background.tex` |
| 28 | Edge features in/out of message passing | `02_background.tex` |
| 29 | NLL Gaussian constant note | `02_background.tex` |
| 30 | Adaptive conformal `σ + ε` | `02_background.tex` |
| 32 | `1/√2` formatting | Multiple |
| 33 | Combined uncertainty units | `03_methodology.tex` |

**Phase C subtotal: ~45 min**

---

## Phase D: STYLE + WORDING POLISH — 90 min

| # | Issues | Where |
|---|---|---|
| 34-46 | Front matter, abstract, contributions polish | `pages/`, `01_introduction.tex` |
| 47-59 | Chapter 5 wording fixes | `05_results.tex` |
| 60-72 | Chapter 6 wording fixes | `06_discussion.tex` |
| 73-80 | Conclusion + Appendix polish | `07_conclusion.tex`, `appendix_a_master_table.tex` |

**Phase D subtotal: ~90 min**

---

# PART 2 — Chapter-by-Chapter Checklist

## Chapter 1 — Introduction (`01_introduction.tex`)

- [ ] **#39:** Align "six UQ methods" taxonomy with Section 3.3 (rephrase as "six post-hoc methods" or "five post-hoc + three uncertainty-aware extensions")
- [ ] **#40:** Contribution 2: distinguish pooled ρ=0.4820 from mean per-graph ρ=0.464 with CI [0.460, 0.469]
- [ ] **#41:** Figure 1.1: change "Reproduced from Natterer..." to "Adapted from Natterer..." if modified

## Chapter 2 — Background (`02_background.tex`)

- [ ] **#26:** Line 13: `G=(V,E,X,E)` — change second `E` (edge features) to `\mathbf{F}` or `\mathbf{Z}`
- [ ] **#27:** Define `N(v) = {u : (u,v) ∈ E}` — clarify directed (incoming) vs undirected
- [ ] **#28:** If edge features unused in message passing, remove from `\mathcal{G}` definition
- [ ] **#29:** NLL equation L46: add note "Gaussian normalising constant `1/2 log(2π)` omitted"
- [ ] **#30:** Adaptive conformal score: ensure `σ + ε` denominator (L40)
- [ ] **#43:** Soften "MC Dropout = epistemic" — call it "empirical uncertainty signal that approximates epistemic uncertainty"

## Chapter 3 — Methodology (`03_methodology.tex`)

- [ ] **#1:** Table 3.1 caption (L22): "training set" → "test set" OR change number to 25,308,000
- [ ] **#9:** Table 3.2 caption (L46): clarify `pos ∈ R^(N×3×2)` (start/end/midpoint, model uses start+end)
- [ ] **#9 cont:** Main text (L41): "...consume per-node start and end coordinates **(midpoint stored but unused)**"
- [ ] **#31:** L110 — remove "(Equation~\eqref{eq:hetero_nll_bg}'s reliability counterpart)"
- [ ] **#33:** L46 NLL: explicitly state Gaussian constant omitted
- [ ] **#44:** Add `CAPACITY_REDUCTION` sign: "negative values represent reductions"
- [ ] **#45:** Table 3.1 caption: clarify "Mean/Std from StandardScaler; Median from raw distribution"
- [ ] **#46:** HIGHWAY exclusion: add "may remove useful road-type signal — accepted to maintain comparability with Natterer (2025)"
- [ ] **#47:** Figure 3.2 "MLP Head" → "Final layer (GATConv for T2-T8, Linear for T1)"
- [ ] **#48:** Add explicit dropout-active-stages note in Figure 3.2 caption

## Chapter 4 — Experimental Setup (`04_experiments.tex`)

- [ ] **#2:** Reconcile "160-180 batch files" with "200 batches imply 10K scenarios" — say "approximately 200 batches"
- [ ] **#3:** Add: "Selecting the first 20 batches assumes batch ordering is uncorrelated with scenario properties; if ordering reflects collection order, mild subset-selection bias is possible. Future work would resample 1,000 scenarios uniformly at random across all batches."
- [ ] **#4:** Reword T8 selection: "Trial 8 attained the highest test R² among UQ-compatible trials and was selected as primary backbone for subsequent UQ analyses; ideally selection would have been based on validation R² to avoid test-set peeking."
- [ ] **#12:** Add justification for `Q̂ > 0` gate: "Negative Q̂ is not theoretically invalid but indicates the trained quantile head already over-covers the calibration set; treated here as a practical sanity check that conformal correction is contributing positively to coverage."
- [ ] **#49:** Table 4.2 column header: "Dropout" → "Effective dropout"
- [ ] **#50:** Add formula: `L_weighted = (1/n) Σ w_i (y_i - ŷ_i)²` and define weights
- [ ] **#51:** Confirm validation R² used for early stopping; if so, mention val R² alongside test R² in T8 selection
- [ ] **#52:** Trial D — explicitly state "deterministic inference with dropout disabled"
- [ ] **#22:** Trial 9 runtime caveat: "frozen backbone still requires forward pass through full 1.4M parameters"

## Chapter 5 — Results (`05_results.tex`)

### 5.1
- [ ] **#5:** Add caveat: "T1-T6 (50 test graphs, 80/15/5) and T7-T8+ (100 test graphs, 80/10/10) results are presented in the same table for comparison; cross-group differences include a test-set composition component beyond architectural choice."
- [ ] **#6:** Fix wording: "the seven UQ-compatible trials (T2-T8 with non-zero dropout and GATConv output)" → "**the five dropout-enabled GATConv trials (T2, T5, T6, T7, T8)**" (excluding T3, T4 with dropout=0)
- [ ] **#71:** "T1's higher accuracy is partly attributable to..." → "T1's higher accuracy **may be attributable to**..."
- [ ] **#72:** "T1 incompatible because Linear head" → "T1 incompatible because effective dropout is zero (Linear head reinforces this but is not the primary cause)"

### 5.2
- [ ] **#23:** Mention global ρ may be inflated by zero-effect Q1 nodes; cross-reference Section 5.10
- [ ] **#43:** "MC Dropout captures epistemic uncertainty" → "MC Dropout serves as an empirical uncertainty ranking signal"
- [ ] **#53:** "Negligible accuracy" → "small accuracy change (R² 0.5957 → 0.5856, MAE essentially unchanged)"

### 5.3
- [ ] **#14:** "near-exact marginal coverage" — add "(empirical, on the held-out evaluation graphs)"
- [ ] **#42:** "Standard conformal **over-covers** low-σ nodes" → "Standard conformal **can over-cover** low-σ nodes (98.1% on D1 in this setting)"
- [ ] **#54:** Table 5.2 add explanation: "Empirical k_p > Gaussian k_p means σ underestimates error spread (underdispersion)."
- [ ] **#55:** Footnote: "k₉₅ before/after temperature scaling computed on identical 70% evaluation subset for fair comparison"

### 5.4
- [ ] **#56:** Move Figure 5.5 to Section 5.3 (use `[h!]` placement) OR add reference: "Figure 5.5 (in Section 5.3) shows the conditional coverage discussed there."

### 5.5
- [ ] **#10:** Reconcile AUROC: text says 0.7548; Figure 5.10 shows 0.7538. Update Figure 5.10 caption to match 0.7548 (canonical from `auroc_corrected.json`). Same for top-20% (0.7324) and T7 values.
- [ ] **#57:** Winkler caption: "conformal calibration **improves interval quality at fixed coverage**" not "tightens intervals"
- [ ] **#58:** Add: "Conformal correction expands intervals symmetrically around prediction; it does not shift the centre. For asymmetric tails, CQR (Trial 11) is required."

### 5.6
- [ ] **#7:** Trial D explanation: "Each Deep Ensemble member is trained from scratch with a different random seed but identical hyperparameters; member R² values lie in [0.640, 0.650]. T8's lower 0.5957 reflects a different training run, not different hyperparameters — likely sensitivity to data shuffling order or weight initialisation seed."
- [ ] **#65-66:** Soften "samples from approximate posterior" → "produces stochastic forward passes that empirically yield uncertainty more correlated with error than seed-only ensemble disagreement"
- [ ] **#25:** Confirm: "Experiment B ensemble members all evaluated on the 100-graph T7-T8 test set" — this requires verification because T2/T5/T6 originally used 50-graph split

### 5.7
- [ ] **#16, #43:** Soften Trial 9 aleatoric interpretation:
  - Figure 5.14 caption: replace "reflects genuine traffic-flow variability" with "T9 attributes most predicted uncertainty to its aleatoric component. Whether this corresponds to irreducible noise or to NLL-driven σ inflation on hard examples (Seitzer 2022) cannot be distinguished without ground-truth uncertainty."
- [ ] **#60:** Section 5.7 paragraph: "directly demonstrates" → "consistent with the NLL-MSE trade-off (Seitzer 2022)"
- [ ] **#79:** Table 5.4: k₉₅ row marked "lower better" — this is diagnostic, NOT a gate. Add table footnote.

### 5.8
- [ ] **#20:** Mention T10-v1 numbers briefly: "T10-v1 (lr 5×10⁻⁴) collapsed further to R²=0.315; T10-v2 (lr 5×10⁻⁵) is the more favourable variant reported here"

### 5.9
- [ ] **#11:** "R² drops by only 1.2% from T8" → "R² drops from 0.5957 to 0.5835 — an absolute difference of 0.0122 R² points (~2.0% relative)"
- [ ] **#21:** Add caveat: "**T11 preserves R² but MAE rises** (3.957 → 4.302 veh/h). Quantile-midpoint prediction trades MAE for asymmetric interval coverage."
- [ ] **#61:** Comparison clarification: "T10-v2 (lr=5e-5) and T11 (lr=5e-4) — backbone trainability is the headline difference, but learning rate also differs. Strictly, T10-v2 vs an unfrozen-T11 with lr=5e-4 would be the cleanest isolation; this isolated experiment was not run."

### 5.10
- [ ] **#24, #67-68:** Soften:
  - "saturation effects" → "saturation-related effects (likely mechanism)"
  - "absolute error dwarfs σ" → "absolute error spans a wider range than σ in this regime"
  - "several orders of magnitude" → "wide dynamic range"

### 5.11
- [ ] No major fixes; minor wording polish.

## Chapter 6 — Discussion (`06_discussion.tex`)

- [ ] **#13, #70:** RQ5: "Yes, **if and only if** the MSE-trained backbone is kept frozen" → "**The evidence in this thesis supports** keeping the backbone frozen when adding uncertainty-aware extensions."
- [ ] **#63:** Section 6.1: "Trials 9, 10, 11 differ only in what gets fine-tuned" → "Of the three uncertainty-aware extensions, **only Trial 10-v2 vs Trial 11 isolates backbone trainability** (same head, same loss, same data). Trial 9 differs from both in head architecture and loss function."
- [ ] **#64:** "optimally encoded" → "learned useful representations under MSE"
- [ ] **#65-66:** Soften causal explanations of MC Dropout vs Deep Ensemble — use "empirically" and "consistent with"
- [ ] **#67-68:** Stratified UQ mechanisms — say "likely mechanisms include..."
- [ ] **#14, #69:** Section 6.5 — strengthen exchangeability discussion already present; soften "guarantee" to "empirical marginal coverage"
- [ ] **#73:** Define GEBM: "GEBM (Graph Energy-Based Models, Fuchsgruber et al. 2024)"

## Chapter 7 — Conclusion (`07_conclusion.tex`)

- [ ] **#15, #74:** Replace problematic sentences:
  - "None of these methods is expensive" → "**These methods are tractable for offline policy evaluation**; MC Dropout's S=30 inference (~228 minutes for 100 graphs) and Deep Ensemble's 5× training cost are not negligible but are within feasible budgets for the policy-design loop."
  - "all are model-agnostic" → "**all are post-hoc on the trained backbone** (with the exception of CQR, which trains a small new head)"

## Appendix A (`appendix_a_master_table.tex`)

- [ ] **#75:** Verify bold values render bold in PDF
- [ ] **#76:** Add note at top: "T1-T6 evaluated on 50 test graphs (80/15/5 split); T7-T11 and Deep Ensemble on 100 test graphs (80/10/10 split). Cross-group comparisons should be interpreted descriptively."
- [ ] **#77:** Adaptive conformal "PICP 89.87%" — note "(slightly below 90% nominal target)"
- [ ] **#78:** CRPS formula: ensure `1/√2` and `≈ 0.707` render correctly
- [ ] **#79:** Add gate-table footnote: "k₉₅ entries are diagnostic, not gates"

## Front matter (`pages/`)

- [ ] **#34:** Acknowledgments AI tool declaration: list specific tools "Grammarly, ChatGPT/Claude (matplotlib formatting and grammar refinement)"
- [ ] **#35:** Abstract: adaptive conformal "[59,98]→[83.7,96.4]" — add "at the 90% nominal level"
- [ ] **#36:** Abstract: "passes all six gates" → "passes all six CQR go/no-go gates"
- [ ] **#37:** German: "Posthoc" → "Post-hoc"
- [ ] **#38:** German: "unsicherheits-bewusste" → "unsicherheitsbewusste"

---

# PART 3 — Exact Replacement Wording (Top 15 Critical Fixes)

## Fix 1: Table 3.1 caption (Issue #1)

**File:** `03_methodology.tex` Line 22

**REPLACE:**
```latex
Raw-unit statistics for the five input features ($n = 3{,}163{,}500$ nodes from the training set).
```

**WITH:**
```latex
Raw-unit statistics for the five input features computed across the 100-graph test set
($n = 3{,}163{,}500$ nodes; 100 scenarios $\times$ 31{,}635 segments).\
Mean and standard deviation are read from the fitted T8 \texttt{StandardScaler} (which was fit on the training partition);
median is computed from the raw test-set distribution.
```

---

## Fix 2: Table 3.2 caption + main text — pos shape (Issue #9)

**File:** `03_methodology.tex` Line 41 (main text) + Line 46 (table caption)

**REPLACE main text (L41):**
```latex
The first two layers are PointNetConv layers that consume per-node start and end coordinates.
```

**WITH:**
```latex
The first two layers are PointNetConv layers that consume per-node start and end coordinates;
the input data tensor additionally stores a midpoint coordinate (preserving the original
preprocessing of \textcite{natterer2025ml}) but the current PointNetTransfGAT architecture
does not use it.
```

**REPLACE Table 3.2 caption:**
```latex
Input: node features $\mathbf{x} \in \mathbb{R}^{N \times 5}$ and positional coordinates $\mathbf{pos} \in \mathbb{R}^{N \times 3 \times 2}$.
```

**WITH:**
```latex
Input: node features $\mathbf{x} \in \mathbb{R}^{N \times 5}$ and positional coordinates
$\mathbf{pos} \in \mathbb{R}^{N \times 3 \times 2}$, where the three coordinate slots correspond to
segment \emph{start, end, and midpoint}; the architecture below consumes the start and end coordinates only.
```

---

## Fix 3: Section 3.4 — Equation reference (Issue #31)

**File:** `03_methodology.tex` Line 110

**REPLACE:**
```latex
Calibration is reported via the Kuleshov ECE (Equation~\eqref{eq:hetero_nll_bg}'s reliability counterpart),
```

**WITH:**
```latex
Calibration is reported via the Kuleshov ECE~\autocite{kuleshov2018accurate},
```

---

## Fix 4: Section 5.1 — UQ-compatible trial set (Issue #6)

**File:** `05_results.tex` Section 5.1 paragraph 1

**REPLACE:**
```latex
Among the seven UQ-compatible trials (T2--T8, non-zero dropout, GATConv output), T8 is the strongest
```

**WITH:**
```latex
Among the five dropout-enabled GATConv trials compatible with MC Dropout (T2, T5, T6, T7, T8 — T3 and T4 disabled dropout entirely), T8 is the strongest
```

---

## Fix 5: Section 5.9 — T11 R² wording (Issue #11)

**File:** `05_results.tex` Section 5.9

**REPLACE:**
```latex
$R^2$ drops by only $1.2\%$ from T8
```

**WITH:**
```latex
$R^2$ drops from T8's $0.5957$ to $0.5835$ — an absolute difference of $0.0122$ ($\approx 2.0\%$ relative)
```

**ADD after the gate table:**
```latex
\paragraph{MAE caveat.}\ T11's quantile-midpoint MAE is $4.302$~veh/h, slightly above T8's $3.957$~veh/h. Quantile-midpoint prediction does not minimise squared error; the slight MAE penalty is the price for asymmetric-interval coverage.
```

---

## Fix 6: Section 5.7 — T9 aleatoric interpretation (Issue #16)

**File:** `05_results.tex` Figure 5.14 caption

**REPLACE:**
```latex
This pattern means most of the prediction uncertainty in Trial~9 reflects genuine traffic-flow variability rather than gaps in what the model has learned.
```

**WITH:**
```latex
This pattern means Trial~9 \emph{attributes} most of the predicted uncertainty to its aleatoric component. Whether this corresponds to genuinely irreducible traffic-flow noise or to the well-known NLL pitfall of $\hat\sigma$ inflation on hard examples~\autocite{seitzer2022pitfalls} cannot be distinguished without ground-truth uncertainty labels; the safer reading is the former.
```

---

## Fix 7: Section 6.7 — RQ5 wording (Issues #13, #70)

**File:** `06_discussion.tex` Section 6.7 RQ5 answer

**REPLACE:**
```latex
\textbf{RQ5...} Yes, if and only if the MSE-trained backbone is kept frozen.
```

**WITH:**
```latex
\textbf{RQ5...} The evidence in this thesis strongly supports keeping the MSE-trained backbone frozen when adding uncertainty-aware extensions.
```

---

## Fix 8: Section 6.1 — only T10-v2 vs T11 isolates (Issue #63)

**File:** `06_discussion.tex` Section 6.1 (search for "Trials 9, T10-v2, and 11")

**REPLACE:**
```latex
All three sit on top of the T8 MSE-trained backbone (Section~\ref{sec:trial_results}) with a new output head, and they differ only in what gets fine-tuned.
```

**WITH:**
```latex
All three sit on top of the T8 MSE-trained backbone with a new output head. Trial~9 differs from Trials~10 and~11 in both head architecture (heteroscedastic vs CQR) and loss function (NLL vs pinball). Within the CQR family, \emph{only the comparison T10-v2 vs T11 isolates backbone trainability as the single design knob}: same head, same loss, same data, differing solely in whether pinball-loss gradients reach the backbone.
```

---

## Fix 9: Section 7 — Conclusion overclaim (Issues #15, #74)

**File:** `07_conclusion.tex` (paragraph 2)

**REPLACE:**
```latex
None of these methods is expensive in compute terms, and all are model-agnostic.
```

**WITH:**
```latex
These methods are tractable within an offline policy-evaluation loop. MC Dropout costs roughly $30\times$ the inference of a single deterministic forward pass; the Deep Ensemble costs $\approx 5\times$ training and $5\times$ inference; the frozen-backbone CQR head adds 134 trainable parameters and a single deterministic pass at deployment. All are post-hoc on top of an MSE-trained backbone, with CQR additionally training a small new head.
```

---

## Fix 10: Section 5.6 — Deep Ensemble vs T8 R² discrepancy (Issue #7)

**File:** `05_results.tex` Section 5.6 (Trial D paragraph)

**INSERT after "Individual member $R^2$ values lie in $[0.640, 0.650]$":**
```latex
The lower R² of T8 itself ($0.5957$) reflects a different training run with different random initialisation and data-shuffling order; T8 was trained earlier in the project and not reproduced as part of the Deep Ensemble batch. The within-Ensemble R² range ($[0.640, 0.650]$) is therefore a more reliable estimate of the per-member capability under the T8 hyperparameter configuration than T8's own R² value.
```

---

## Fix 11: Section 6.5 — exchangeability wording (Issues #14, #69)

**File:** `06_discussion.tex` Section 6.5

The current text is already cautious; the additional fix is to ensure RQ4 in Section 6.7 also uses "empirical" framing:

**REPLACE in Section 6.7 RQ4:**
```latex
Split conformal on T8 achieves near-exact marginal coverage
```

**WITH:**
```latex
Split conformal on T8 achieves near-exact \emph{empirical marginal coverage on the 50 evaluation graphs}; the formal conformal guarantee rests on exchangeability, which holds at the scenario level but not strictly at the node level (Section~\ref{sec:exchangeability})
```

---

## Fix 12: Section 5.5 — AUROC reconciliation (Issue #10)

**File:** `05_results.tex` Section 5.5 + Figure 5.10 caption

**Action:** Confirm canonical values from `auroc_corrected.json`:
- T8 top-10%: 0.7548 (text correct)
- T8 top-20%: 0.7324 (text correct)
- T7 top-10%: 0.7416 (text correct)
- T7 top-20%: 0.7151 (text correct)

**FIX Figure 5.10 caption:**

Update displayed AUROC values to match text and Appendix A.2:
```
Panel (a): T8 AUROC = 0.7548; T7 AUROC = 0.7416
Panel (b): T8 AUROC = 0.7324; T7 AUROC = 0.7151
```

(Figure source must be regenerated with consistent rounding.)

---

## Fix 13: Section 4.1 — corpus + subset bias (Issues #2, #3)

**File:** `04_experiments.tex` Section 4.1, "A note on the 10\% subset" paragraph

**REPLACE:**
```latex
The full Natterer corpus is distributed as roughly 160--180 batch files of 50 graphs each. This thesis loads the first 20 batches, which yields the $1{,}000$-scenario subset
```

**WITH:**
```latex
The full Natterer corpus consists of approximately 200 batch files of 50 graphs each (totalling $\approx 10{,}000$ scenarios). This thesis loads the first 20 batches, yielding the $1{,}000$-scenario subset. \emph{Selecting the first 20 batches presumes that batch ordering is uncorrelated with scenario properties (capacity-reduction magnitude, affected-segment selection); if ordering reflects collection or generation order, mild subset-selection bias is possible.} A natural follow-up is to draw a uniformly-random 1{,}000-scenario subset across all batches and verify that the relative method comparisons reported here are preserved.
```

---

## Fix 14: Background `G=(V,E,X,E)` (Issue #26)

**File:** `02_background.tex` Line 13

**REPLACE:**
```latex
A graph $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathbf{X}, \mathbf{E})$ has node features $\mathbf{X}$ and edge features $\mathbf{E}$
```

**WITH:**
```latex
A graph $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathbf{X})$ has node features $\mathbf{X}$ (edge features are not used by the architecture in this thesis)
```

OR if edge features are used somewhere:
```latex
A graph $\mathcal{G} = (\mathcal{V}, \mathcal{E}, \mathbf{X}, \mathbf{F})$ has node features $\mathbf{X}$ and edge features $\mathbf{F}$
```

---

## Fix 15: Front matter / abstract polish (Issues #35, #36, #37, #38)

**File:** `pages/abstract.tex` (English abstract)

- "Adaptive conformal narrows conditional coverage from [59.0%, 98.1%] to [83.7%, 96.4%]" → add "**at the 90% nominal level**"
- "passes all six gates" → "**passes all six CQR go/no-go gates**"

**File:** `pages/zusammenfassung.tex` (German abstract)

- "Posthoc" → "Post-hoc" (with hyphen)
- "unsicherheits-bewusste" → "unsicherheitsbewusste" (no hyphen)

---

# PART 4 — Tables and Figures to Update

| Asset | Issue # | Action |
|---|---|---|
| Table 3.1 caption | 1, 45 | Fix "training" → "test"; clarify Mean/Std vs Median source |
| Table 3.2 caption | 9 | Add 3-coordinate (start/end/midpoint) clarification |
| Table 4.2 | 49 | Column header "Dropout" → "Effective dropout"; consider footnote on T3/T4 replication |
| Table 5.1 caption | 5 | Add cross-group split caveat |
| Table 5.2 | 54 | Add explanatory note on underdispersion |
| Table 5.4 | 79 | Footnote: k₉₅ row diagnostic, not a gate |
| Figure 1.1 caption | 41 | "Reproduced" → "Adapted" if modified |
| Figure 3.2 | 47, 48 | "MLP Head" → "Final layer (GATConv/Linear)"; mark dropout-active layers |
| Figure 5.5 | 56 | Move to Section 5.3 (use [h!]) or add cross-reference |
| Figure 5.10 | 10 | Update AUROC values to match text (0.7548, 0.7324, 0.7416, 0.7151) |
| Figure 5.13 caption | 59 | Soften "T8 close behind Deep Ensemble" — quantify gap |
| Figure 5.14 caption | 16 | Soften aleatoric "genuine traffic noise" claim |
| Figure 5.15 placement | (5.10-B) | Verify in Section 5.9 (Trial 11) not 5.10 |
| Figure 5.17 caption | — | Already states "illustrative" — fine |
| Appendix A.6 | 79 | Mark k₉₅ as diagnostic |

---

# PART 5 — Viva Defense Risk List with Prepared Answers

## RISK 1 (HIGHEST): Data scale (10% subset)

**Likely question:** "How can we trust your findings when you only used 10% of the data?"

**Prepared answer:**
> "The 1,000-scenario subset reflects a compute constraint (single T4 GPU, ~131 hours total). Critically, the thesis structures comparisons so all methods see the same 1,000 scenarios — relative method differences (MC Dropout vs Deep Ensemble, T10 vs T11) are isolated from data scale. The 100-graph test set provides 3.16M node-level test predictions with bootstrap 95% CI on mean per-graph ρ of width 0.009 — the metric estimates are statistically tight. Mechanism-level findings should generalise to the full corpus; verifying this is the most direct piece of future work."

## RISK 2 (HIGHEST): T1 vs T8 — why use weaker T8?

**Likely question:** "T1 has R²=0.7860 vs T8's 0.5957. Why didn't you use T1?"

**Prepared answer:**
> "Three reasons. First, T1 was trained with `use_dropout=False`, so MC Dropout reduces to a constant function and is undefined on it — making T1 incompatible with the dominant UQ method studied here. Second, T1's higher accuracy may be partly attributable to its Linear final layer's strong inductive bias on the bulk of segments where Δv response is near-linear; this is a property of the T1 training run, not necessarily an architectural superiority. Third, the thesis's research question is uncertainty quantification, not point-accuracy maximisation — for that goal, architectural compatibility with the UQ machinery dominates raw R². T8 is the strongest UQ-compatible model in the T1-T8 family. The architectural confound (Linear vs GATConv, batch, lr) is acknowledged in Section 6.9 as a limitation; a controlled ablation is left as future work."

## RISK 3: Freeze-the-backbone — universal principle?

**Likely question:** "Is freeze-the-backbone a universal rule or specific to your setting?"

**Prepared answer:**
> "I'm careful with scope. The evidence is causally identified for this thesis's specific setting — MSE-trained PointNetTransfGAT backbone with a small head on a 1,000-scenario subset. The mechanism via Seitzer et al. (2022) NLL/MSE trade-off suggests broader applicability, but I have not tested other architectures, losses, or data scales. The thesis describes it as 'an important design consideration' rather than a universal law. Future work would validate it on other architectures, including non-graph models, to determine whether it is a general principle for adapting MSE-trained backbones to uncertainty-aware objectives."

## RISK 4: T3 vs T4 identical hyperparameters

**Likely question:** "Table 4.2 shows T3 and T4 with identical hyperparameters but different R². What is the difference?"

**Prepared answer:**
> "T4 was a replication run of T3 with different random initialisation and data-shuffling order. Both shared identical hyperparameters and the 80/15/5 split. The purpose of T4 was to verify that T3's weighted-MSE failure (R²=0.2246) was systematic rather than a random initialisation artefact. T4's R²=0.2426 — within ~0.02 R² points of T3 — confirms the failure is systematic. The two trials together provide a small replication study showing that weighted MSE without dropout consistently fails at this 1,000-scenario scale."

## RISK 5: Q1 high ρ=0.725 — meaningful?

**Likely question:** "Is your Q1 ρ=0.725 finding really informative, or is it a mechanical artefact?"

**Prepared answer:**
> "It's partly mechanical, and the thesis acknowledges this in Sections 6.4 and 6.8. Q1 contains segments where the policy intervention has no effect — Δv = 0 throughout. When y = 0, both |error| and σ reduce to functions of the model's small output magnitude on unchanged segments, and their correlation is partly an artefact of shared dependence on |ŷ|. The Q1→Q4 contrast is therefore better read as 'MC Dropout works mechanically on trivial segments and breaks on hard ones' than as 'MC Dropout is highly informative on easy regimes'. The substantive degradation on Q4 (ρ=0.100) is real and not mechanical."

## RISK 6: Q4 silent failure — what mitigations?

**Likely question:** "If MC Dropout silently fails on the highest-impact segments (Q4), how can it be deployed?"

**Prepared answer:**
> "Two layers of mitigation are recommended. First, my thesis proposes a three-tier triage policy (Section 5.11): the surrogate is a triage tool, not a MATSim replacement. High-σ predictions — which include most Q4 cases — are routed back to MATSim simulation. Second, future work I propose includes explicit OOD detectors and feature-conditional conformal methods that target the high-|Δv| regime specifically. The honest framing is that the surrogate is reliable on the bulk of segments where the policy has small or no effect, and uncertain in exactly the high-impact regime that planners care most about — so high-impact decisions warrant verification."

## RISK 7: Conformal coverage guarantee under node dependence

**Likely question:** "Conformal prediction requires exchangeability, but your nodes within a graph are highly correlated. Is the guarantee actually valid?"

**Prepared answer:**
> "The formal conformal guarantee rests on exchangeability, which holds at the scenario level (50 calibration / 50 evaluation graphs randomly partitioned with seed 42) but is not strictly satisfied at the node level. The reported coverage should therefore be read as empirical marginal coverage across scenarios and nodes — averaged over both, the observed 90.02% and 95.01% match the nominal targets. Within a single graph, coverage varies in [80.5%, 93.7%] (Section 6.5). A natural extension is graph-level nonconformity scoring, which would restore strict scenario-level exchangeability at the cost of coarser intervals. This is acknowledged as a limitation."

## RISK 8: Multi-model ensemble — Experiment B test set

**Likely question:** "Experiment B averages T2/T5/T6/T7/T8, but T2/T5/T6 used the 50-graph test set and T7/T8 used 100. How are predictions combined?"

**Prepared answer:**
> "Experiment B predictions were generated by running each ensemble member on the **same 100-graph test set** used by T7/T8. T2/T5/T6 models were re-evaluated on this larger test set; the original T2-T6 R² values reported in Section 5.1 were on their original 50-graph splits, so Experiment B's per-member R² differs slightly. The R²-weighted aggregation uses these re-evaluated values for consistency."

## RISK 9: T9 aleatoric attribution — real or NLL artefact?

**Likely question:** "Your Trial 9 shows 99.85% aleatoric-dominant uncertainty. Is that genuine, or is it the NLL-inflation pitfall of Seitzer 2022?"

**Prepared answer:**
> "Strictly speaking, I cannot fully distinguish without ground-truth uncertainty labels. Trial 9 attributes 99.85% of predicted uncertainty to its aleatoric component, but Seitzer et al. (2022) document the NLL pitfall where networks reduce loss by inflating σ̂ on hard examples. My λ=0.01 log-variance regulariser partially mitigates this, but cannot eliminate it when head capacity to improve μ̂ is limited (the 134-parameter constraint here). The safer interpretation is that Trial 9 *attributes* most uncertainty to the aleatoric component — whether this corresponds to genuinely irreducible traffic-flow noise or to NLL-driven inflation is an open question worth future investigation."

## RISK 10: Quadrature combination formula

**Likely question:** "Your text says 'σ_combined = sqrt(σ_MC² + σ_ens²)'. Is that quadrature correctly applied here, given the two signals are correlated?"

**Prepared answer:**
> "The quadrature formula assumes independence of the two variance sources, which holds in the limit if MC Dropout uncertainty and seed-ensemble disagreement come from genuinely independent stochastic mechanisms. The empirical result — combined ρ=0.4909 vs MC Dropout alone 0.4908, an improvement of +0.0001 — is direct evidence that the two signals are highly correlated in practice (both come from stochastic forward passes through the same trained model). Quadrature is not the wrong formula; it's the correct formula but applied to non-independent sources, which is why the gain is negligible. The practical takeaway is that seed-ensemble variance adds essentially no information beyond MC Dropout at this scale."

---

# PART 6 — Recommended Execution Order

```
DAY 1 (today, ~3 hours):
   Morning:
   1. Phase A critical fixes (90 min) — Fixes 1-15 above
   2. PDF compile + visual check
   
   Afternoon:
   3. Phase B methodological fixes (90 min)
   4. Sanity check on numbers consistency

DAY 2 (~2 hours):
   Morning:
   5. Phase C notation polish (45 min)
   6. Phase D wording polish (90 min)
   
   Afternoon:
   7. Final PDF compile
   8. Review-pass with Dominik/Elena (when feedback arrives)
   
DAY 3 (defence prep — not fix-related):
   1. Memorize 5 master findings (Section 6.8)
   2. Memorize 5 RQ answers (Section 6.7)
   3. Practice 10 viva risk answers from Part 5 above
   4. Run mock viva with peer
```

---

# PART 7 — Files Touched Summary

| File | # of fixes |
|---|---|
| `pages/abstract.tex` | 4 |
| `pages/zusammenfassung.tex` | 3 |
| `pages/acknowledgments.tex` | 1 |
| `01_introduction.tex` | 3 |
| `02_background.tex` | 6 |
| `03_methodology.tex` | 11 |
| `04_experiments.tex` | 7 |
| `05_results.tex` | 22 |
| `06_discussion.tex` | 12 |
| `07_conclusion.tex` | 2 |
| `appendix_a_master_table.tex` | 5 |
| `figures/*` | 5 figure regenerations |
| **TOTAL** | **~80 individual edits** |

---

# PART 8 — DO NOT REMOVE / PRESERVE

- **All five primary findings (Section 6.8)** — these are the thesis's core
- **All numerical results in tables** — only update inconsistencies, never data
- **The freeze-the-backbone narrative** — soften "if and only if" but keep the principle
- **The complementarity finding** — Deep Ensemble vs MC Dropout
- **The three-layer calibration cascade** — MC Dropout → temperature scaling → adaptive conformal
- **The three-tier deployment policy (Section 5.11)** — operational framework
- **All audit-verified numbers** — 49 cross-checked between NPZ + JSON

---

**End of Fix Plan**
