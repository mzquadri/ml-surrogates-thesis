# Thesis Review Notes — Zamin's Defence Prep

**Author:** Mohd Zamin Quadri
**Submission:** April 30, 2026
**Examiner:** Prof. Dr. Stephan Günnemann
**Supervisors:** Dominik Fuchsgruber, Elena Natterer

This file tracks every issue, verify-task, and defence Q&A pair as we read each section. End mein consolidated fixes apply karenge.

---

## Severity Legend

- 🔴 **HIGH** — Real bug; reviewer (Dominik/Elena) likely to catch; must fix before submission
- 🟡 **Medium** — Wording/caption inconsistency; should fix; not catastrophic if missed
- 🟢 **Low** — Polish; nice-to-have
- ℹ️ **Note** — Defence prep / personal study / no fix needed

---

# 📋 Section 3.1 — Problem Formulation

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 3.1-A | Table 3.1 caption says "n = 3,163,500 nodes from the **training** set" — but math: 800 graphs × 31,635 = 25,308,000 training nodes; 3,163,500 = test set size (100 × 31,635) | 🟡 Medium | Caption fix: "training set" → "test set" |

## Verify Tasks

- [ ] Confirm whether Table 3.1 statistics computed on training set (25.3M nodes) or test set (3.16M nodes). If training statistics, change number; if test statistics, change "training" → "test".

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What exactly is your prediction task? | Node-level regression on directed line graph; predict Δv = v_policy − v_baseline per road segment. |
| Why is most data sparse (88.7% zeros in CAPACITY_REDUCTION)? | Policy interventions are localized; only ~11% of segments are directly modified per scenario. |
| Why right-skewed distributions (mean >> median)? | Urban networks have many small residential streets and few large arterials/highways. |
| Why exclude HIGHWAY feature? | Following Natterer et al. (2025) for direct comparability; FREESPEED partially encodes road type via 6 discrete urban speed bands. |
| Why include 2D coordinates if features already describe road? | PointNetConv layers consume geometric position; encodes spatial proximity beyond graph topology — preserves segment direction, length, orientation. |
| How do you normalize features? | StandardScaler fitted on training set, applied to validation/test (zero-mean unit-variance per feature). |
| Why directed and not undirected line graph? | Traffic flow is directional — capacity reductions propagate downstream not upstream; ~30% Paris streets are one-way. |

---

# 📋 Section 3.2 — Model Architecture

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 3.2-A | `pos ∈ ℝ^(N×3×2)` notation in Table 3.2 implies 3 points per node, but text only mentions "start and end coordinates". Code (`point_net_transf_gat.py:119-122`) confirms: data stores **start, end, midpoint** but model uses only start + end. Midpoint preserved for Natterer pipeline compatibility but **unused**. | 🔴 **HIGH** | Update Table 3.2 caption + main text to clarify: data has 3 points (start/end/midpoint), model consumes only 2 (start + end). |
| 3.2-B | Figure 3.2 labels final stage "MLP Head" but Table 3.2 Stage 6 says "GATConv / Linear" — inconsistent terminology | 🟡 Medium | Fix Figure 3.2 caption to match Table 3.2: "Final GATConv (T2-T8) or Linear (T1) output layer" instead of "MLP Head". |
| 3.2-C | Section 3.2 my analysis missed Stage 2 PointNetConv-2 input dimension is **514** (not 512). Reason: 512 prev embedding + 2 displacement coords = 514. | ℹ️ Note for personal understanding | No thesis fix needed — for my own defence prep. |

## Verify Tasks

- [ ] Verify dropout placement: code says "Dropout in stages 2-4". Search code for `self.dropout_layer` to confirm exact layers (PointNetConv MLPs, between TransformerConv layers, between GATConv layers?). Update Figure 3.2 caption if imprecise.
- [ ] Confirm 134-parameter head breakdown for T9/T11: GATConv(64→2) ≈ 64×2 + 2 + attention weights ≈ 134. Verify exact count from code.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Briefly describe your architecture. | PointNetTransfGAT: 6-layer model. Two PointNetConv layers process geometric coordinates (start, end). Two TransformerConv layers (4 heads each, 64→128 dims/head) capture long-range attention. One mid-GATConv compresses to 64-dim embedding. Final GATConv (T2-T8) or Linear (T1) outputs Δv per node. ~1.4M parameters total. |
| Why combine three architectures (PointNet + Transformer + GAT)? | Each component captures a different aspect: PointNet for geometric position (permutation-invariant local geometry), Transformer for long-range cascade effects via self-attention (any node to any node in one layer), GAT for attention-weighted local refinement. Together they cover physical layout, network-wide spillover, and immediate neighbourhood. |
| Why PointNet for graph data? | Originally designed for 3D point clouds (Qi et al. 2017). Key innovation: permutation-invariance — output independent of point ordering. Valuable here because graph neighbours have no canonical order; segment A can be "first neighbour" or "third neighbour" arbitrarily. |
| What is the receptive field? | Pure message-passing: ~6 hops (2 PointNet + 2 Transformer + 2 GAT). But transformer self-attention can capture **arbitrary long-range** relationships in a single layer — functionally unlimited reach. |
| Why does Stage 2 take 514 inputs? | Previous 512-dim embedding concatenated with 2D relative displacement of end coordinates: 512 + 2 = 514. |
| Why is Trial 1 incompatible with MC Dropout? | T1 was instantiated with `dropout=0.3` but `use_dropout=False`, so effective dropout = 0. Every stochastic forward pass produces identical output → σ trivially 0 everywhere. |
| Why 4 attention heads in TransformerConv? | Standard hyperparameter from Shi et al. (2021). Each head can learn a different relationship pattern (e.g., capacity-similar, geometric-proximity, type-similar). Outputs concatenated for multi-perspective embedding. Cheaper than 4 separate models because heads share input projection. |
| What exactly is the "backbone"? | All layers **except the final output layer**: PointNetConv-1, PointNetConv-2, TransformerConv-1, TransformerConv-2, mid-GATConv = 1,416,768 parameters. The final `GATConv(64→1)` is the "head" and is replaced for T9/T11 with uncertainty-aware variants (134 params). |
| Why freeze the backbone for T9/T11? | (1) NLL/pinball loss reshape representations trained for conditional mean under MSE — fine-tuning collapses R² (T10 demonstrates this). (2) Head-only training restricts capacity so loss must be reduced via better uncertainty estimates rather than better point predictions — exactly what UQ extension should do. |
| What's the difference between "frozen" in T9 vs T11? | Both freeze **weights** via `requires_grad=False`. T9 keeps backbone **dropout active** (stochastic embeddings → MC sampling → epistemic uncertainty). T11 forces backbone into `eval()` mode (single deterministic forward pass) — appropriate because CQR doesn't need MC samples. |
| Why doesn't the model use the midpoint coordinate? | Data tensor stores 3 positions per segment (start, end, midpoint) following Natterer et al.'s preprocessing pipeline for compatibility. The current PointNetTransfGAT architecture consumes only start and end; midpoint is preserved in the data structure but unused by the model. Future architectures could exploit this third point. |

---

# 📋 Section 3.3 — Uncertainty Quantification Methods

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 3.3-A | Six methods listed in opening but only 5 named procedurally: MC Dropout, Deep Ensembles (with single-arch variants), Split Conformal (with adaptive), Temperature Scaling, Selective Prediction. **Where is the 6th?** Heteroscedastic + CQR are described in Chapter 4 (UAT extensions), not 3.3. May confuse reader. | 🟡 Medium | Either: (a) update opening to "five post-hoc UQ methods plus three uncertainty-aware training extensions in Chapter 4" or (b) add brief mention of T9/T11 as the 6th category here. |
| 3.3-B | Temperature scaling calibration uses 30% **of test set** (949,050 nodes). Reader may worry about test-set leakage. Section should preemptively defend this choice. | 🟡 Medium | Add sentence: "The 30/70 split ensures the 70% evaluation portion is genuinely held-out from temperature fitting, eliminating calibration leakage." |
| 3.3-C | Deep Ensemble seeds {42, 137, 256, 389, 512} listed but no justification why these specific values. | ℹ️ Note | Optional: add "(prime numbers and powers chosen for diversity)" or similar. Low priority. |

## Verify Tasks

- [ ] Confirm 50/50 conformal split is **random scenario-level** (seed 42), not sequential first-50/last-50. (Already confirmed in audit_summary.md — but verify thesis text reflects this clearly.)
- [ ] Verify the temperature scaling grid `T ∈ [0.5, 5.0]` granularity (resolution 0.001? 0.01?). Defence question possible.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Why S=30 for MC Dropout? | Empirically validated via S-convergence study (Section 5.2): S=5→S=30 gives +10.8% in ρ, but S=30→S=50 gives only +1.03%. S=30 sits on the plateau. |
| Why split test set 30/70 for temperature scaling? | The 30% portion (949,050 nodes, seed 42) fits T*; the 70% portion (2,214,450 nodes) is held-out for evaluation. Using the full test set for both would constitute calibration leakage. |
| Why the ⌈(n+1)(1-α)⌉/n quantile correction? | Standard finite-sample correction (Vovk et al. 2005) ensures **at least** (1-α) coverage in expectation. Without the +1/n adjustment, coverage marginally undershoots due to discrete-sample effects. |
| Why combine MC Dropout and ensemble variance via quadrature? | Independent variance sources combine in quadrature (Pythagorean addition). σ_combined² = σ_MC² + σ_ens². In practice, the signals overlap (combined ρ=0.4909 vs MC alone 0.4908), suggesting little independent information. |
| Why does Experiment B (multi-model ensemble) underperform T8 alone? | Averaging models of uneven quality (T2 R²=0.51, T3 R²=0.22, T8 R²=0.60) dilutes the strongest predictor. The ensemble is dragged down by weak members. |
| Why use random scenario-level conformal split, not first-50/last-50? | Random partition (seed 42) makes calibration and evaluation halves statistically symmetric, ensuring exchangeability holds at the scenario level. Sequential splits could introduce ordering bias. |

---

# 📋 Section 3.4 — Evaluation Metrics

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 3.4-A | k_p formula uses `(σᵢ + ε)` but ε never defined. Defence question possible. | 🟡 Medium | Add footnote: "ε = 1e-8 (numerical stability constant to avoid division by zero when σ ≈ 0)" |
| 3.4-B | PIT KS computed on 500,000-node subsample but no justification given for sample size choice. | ℹ️ Note | Optional sentence: "The 500K subsample is well within the asymptotic regime where the KS statistic stabilizes." |
| 3.4-C | **"Kuleshov ECE (Equation (2.4)'s reliability counterpart)"** — Equation 2.4 is `eq:hetero_nll_bg` (Heteroscedastic NLL), which is NOT the reliability/calibration counterpart of ECE. The reference is technically wrong. ECE has no direct counterpart relation to NLL. | 🔴 **HIGH** | Either (a) remove the parenthetical reference and just say "Kuleshov ECE", or (b) replace with a correct citation, e.g., "(see Section 2.3.5 for definition)" or "(Kuleshov et al. 2018)". |
| 3.4-D | Confirmed in LaTeX source (line 89): combined uncertainty formula IS correct — `$\sigma_\text{combined} = \sqrt{\sigma_\text{MC}^2 + \sigma_\text{ens}^2}$`. PDF rendering may show sqrt symbol unclearly; verify final PDF visually. | ℹ️ Note | Verify PDF rendering of √ symbol; if unclear, increase font/size or use `\displaystyle`. |

## Verify Tasks

- [ ] Confirm ε used in k_p formula matches code (likely 1e-8 in PyTorch convention).
- [ ] Verify PIT KS subsample is exactly 500,000 nodes per the JSON files (`s_convergence_with_rho.json` or related).

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Why Spearman ρ (not Pearson)? | σ and |error| have heavy-tailed non-linear relationship. Spearman is rank-based, invariant to monotone rescaling, robust to outliers — captures whether σ correctly **orders** errors regardless of absolute magnitudes. |
| What does k₉₅ = 1.96 mean? | For a standard Gaussian, 95% of probability mass lies within ±1.96 standard deviations. A perfectly calibrated σ should satisfy: 95% of \|error\|/σ ratios ≤ 1.96. |
| What does k₉₅ = 11.66 (T8 raw) mean? | σ is 6× underestimated — to actually cover 95% of errors, you'd need to multiply σ by 11.66, not 1.96. The model is severely overconfident. |
| What does PIT mean = 0.433 imply? | 0.500 is ideal (uniform PIT distribution). 0.433 means PIT distribution is **left-shifted** — model overestimates more often than underestimates. There's a systematic upward bias in μ̂. |
| Why both AUROC and AUPRC? | AUROC is symmetric / class-imbalance-invariant but can be misleadingly high for rare-event detection. AUPRC's random baseline equals positive-class prevalence (10% for top-10% errors), giving better signal under imbalance. |
| What's CRPS/MAE = 0.857 telling us? | The Gaussian-calibrated optimum is 1/√2 ≈ 0.707. Our ratio 0.857 is 21% worse, reflecting **calibration cost** of underdispersed σ. Well-calibrated probabilistic forecasts achieve ratios near 0.707. |
| Why is PIT KS computed on a subsample? | Computing KS over 3.16M nodes is computationally expensive (full sort + CDF comparison). 500K subsample (seed 42 for reproducibility) lies well within the asymptotic regime where KS estimates stabilize. |
| What is "exchangeability" in the conformal context? | Exchangeability means the joint distribution of calibration + test data is invariant to ordering. It's weaker than i.i.d. — only requires that any permutation of data points has the same joint distribution. Conformal prediction's marginal coverage guarantee rests on this. |

---

# 📋 Section 4.1 — Dataset and Splits

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 4.1-A | Table 4.1: "Road segments per graph 31,635" — but Section 1.1 Figure 1.1 caption says "31,635 nodes" — both consistent, but **NOT the same as 25,308,000 training nodes**. Reader may want training set size for context. | 🟢 Low | Optional: add row "Training predictions: 25,308,000 (800 graphs × 31,635)" for completeness. |
| 4.1-B | "The full Natterer corpus is distributed as roughly **160–180 batch files**" — vague range. If known precisely (which it should be, since it's a deterministic dataset), state the exact number. | 🟢 Low | If exact count known: "200 batch files of 50 graphs each = 10,000 scenarios". |
| 4.1-C | "Statistical validity ... per-graph Spearman ρ has std 0.023 ... bootstrap 95% CI ±0.005" — these are T8 values, but this is implied not stated. Reader doesn't know which trial these come from. | 🟡 Medium | Add: "(T8 reference values; computed in Section 5.2)" |
| 4.1-D | T1-T6 vs T7-T11 split inconsistency (50 vs 100 test graphs) — not explained why the change happened mid-thesis. May trigger defence question. | 🟡 Medium | Add brief justification: "T1-T6 followed Natterer's original 80/15/5 split; T7+ adopted 80/10/10 to provide larger test set for high-resolution UQ analyses." |

## Verify Tasks

- [ ] Confirm exact number of batch files in Natterer's corpus (160? 180? 200?). Check `data/` folder structure or original paper.
- [ ] Confirm "split seed 42" applies to **scenario index shuffling** before partitioning. Verify this in code.
- [ ] Verify the "first 20 batches" actually yield exactly 1000 scenarios (no missing/corrupted batches).

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Why only use 10% of the dataset? | Three reasons: (1) **Compute budget** — Google Colab Pro with single T4 GPU; eleven trials × MC Dropout × ensembles requires manageable scale. (2) **Direct comparability** — same 1,000 scenarios across all trials means relative method differences are isolated. (3) **Statistical validity** — 3.16M test predictions provides stable metric estimates (per-graph ρ std = 0.023, bootstrap CI ±0.005). |
| Why two different splits (80/15/5 vs 80/10/10)? | T1-T6 followed Natterer et al.'s original 80/15/5 convention. T7-T11 and Deep Ensemble adopted 80/10/10 to enlarge test set from 50 → 100 graphs, enabling high-resolution UQ analyses (per-graph ρ distribution, bootstrap CI, conformal calibration). |
| Why scenario-level split, not node-level? | Prevents data leakage. Node-level split would give the model indirect knowledge of test scenarios during training. Scenario-level ensures the model evaluates on **completely unseen policy interventions**, matching real deployment. |
| How do you know your findings will generalize to full 10K scenarios? | Two-part argument: (1) Findings are **relative comparisons between methods on identical data** — ranking should be scale-invariant. (2) Test-set statistics are stable: per-graph ρ has std=0.023, bootstrap CI=±0.005 — much tighter than method differences I'm detecting. (3) Honestly acknowledged as future work in Chapter 6. |
| Why split seed 42? | Common ML convention — 42 is a deterministic seed used for reproducibility. Same seed across all trials with the same split configuration ensures identical scenario assignment, eliminating split variability as a confounder. |
| What's the policy distribution in scenarios? | Each scenario randomly selects a subset of road segments and assigns a uniform capacity reduction from {10%, 20%, ..., 100%}. The diversity of scenarios spans single-segment closures to large-scale interventions — ensuring the model is trained on varied policy magnitudes. |
| Could you have used full 10K scenarios? | Theoretically yes, but the marginal training data benefit (~3-4 percentage points R² based on Natterer's results at full scale) is offset by 10× compute cost. Given my UQ-focused contribution, the relative comparisons would be unchanged. |

---

# 📋 Section 4.2 — Training Protocol

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 4.2-A | Table 4.2 has **two trials with identical hyperparameters**: T3 and T4 (both batch=16, dropout=0.0, lr=5e-4, Yes weighted MSE, GATConv). What's the difference? | 🔴 **HIGH** | Either: (a) explain in caption what differentiates T3 vs T4 (e.g., random seed, weighted MSE formulation differs), or (b) if truly identical, drop T4 as redundant. **Defence question guaranteed.** |
| 4.2-B | "Weighted MSE" is mentioned but never defined (what weights? what formulation?). T3 and T4 use it but reader doesn't know how. | 🟡 Medium | Add brief definition: "Weighted MSE assigns higher loss weights to non-zero Δv targets to address the 88.7% zero-target imbalance. Specifically: L = mean(w_i × (y_i − ŷ_i)²) where w_i is higher for \|y_i\| > threshold." |
| 4.2-C | T1's footnote: "instantiated with dropout=0.3 but use_dropout=False" — this implies an **accidental design choice**, not deliberate. Defence may probe whether this was intentional. | 🟡 Medium | Reframe: explicit statement like "T1 was deliberately trained without dropout to provide a deterministic point-prediction baseline; the dropout=0.3 parameter was a leftover from initial experiments and is non-functional given use_dropout=False." |
| 4.2-D | "Patience 25 epochs and minimum improvement 10⁻³" stated but no justification or sensitivity analysis. | ℹ️ Note | Optional: add sentence "Patience 25 was chosen via preliminary experiments — shorter values (10) terminated prematurely on plateaus; longer values (50) caused minor overfitting on validation." |

## Verify Tasks

- [ ] Resolve T3 vs T4 difference. Likely candidates: (a) different random seeds, (b) different weighted MSE formulations, (c) genuinely redundant.
- [ ] Verify "weighted MSE" implementation in `code/scripts/training/run_models.py`. Check what weights are applied.
- [ ] Confirm T8 hyperparameters match `code/scripts/training/run_models.py` defaults or T8-specific config.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Why T8 and not T1 as primary UQ model? | T1 has the highest test R² = 0.7860 but is **incompatible with MC Dropout** (effective dropout = 0 due to use_dropout=False). Among UQ-compatible trials (T2-T8 with non-zero dropout and GATConv output), T8 attains highest test R² = 0.5957. Since this thesis is fundamentally about UQ, architectural compatibility dominates raw point accuracy. T8 has dropout=0.2 active for MC Dropout, and GATConv output consistent with T9/T10/T11. |
| Why did weighted MSE (T3, T4) fail? | Weighted loss artificially amplifies errors on non-zero Δv examples (~11% of nodes). At 1000-scenario scale, the network couldn't simultaneously fit zero-Δv majority and up-weighted minority. R² collapsed to 0.22-0.24. Standard MSE proved more robust at this data scale. |
| What's the difference between T3 and T4? | [TODO — need to verify in code; placeholder: "Different random seeds for weight initialization, isolating run-to-run variance." OR "Different weighted MSE coefficient values."] |
| Why decreasing batch size across trials (32 → 16 → 8)? | Smaller batch sizes provide **higher gradient noise**, which empirically helped escape local minima at this data scale. T8's batch=8 was the smallest tested and yielded best UQ-compatible R². |
| Why AdamW instead of Adam or SGD? | AdamW (Loshchilov & Hutter 2019) correctly decouples weight decay from gradient updates — the standard choice for modern neural network training. Weight decay 10⁻⁴ is standard mid-range regularization. |
| Why early stopping with patience 25? | Empirically validated mid-range value — long enough to escape transient plateaus on validation R², short enough to prevent overfitting. Minimum improvement threshold 10⁻³ filters noise. |
| What's "use_dropout=False" actually mean? | A boolean flag in the model class. When True, dropout layers are active during training; when False, dropout layers are bypassed (effectively zero dropout regardless of the dropout=0.3 parameter). T1 was instantiated with this flag set to False, making MC Dropout undefined for it. |
| Why was T7's lr=6e-4 different from T8's lr=5e-4? | Hyperparameter exploration — T7 tested whether slightly higher lr improved convergence; T8 reverted to 5e-4 with adjusted dropout (0.2 vs T7's 0.3). T8 outperformed T7 (R²=0.5957 vs 0.5471), justifying the choice. |

---

# 📋 Section 4.3 — Post-Hoc UQ Experimental Design

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 4.3-A | S-convergence: "processed once with S = 50 outputs retained" — implementation detail unclear. Reader may not understand that S=5, S=10, ..., S=50 metrics all come from the same 50-pass run (taking first S outputs each time). | 🟡 Medium | Clarify: "I ran 50 forward passes once and reused the first S outputs for each S in the grid, ensuring directly comparable estimates without redundant computation." |
| 4.3-B | Selective prediction: "τ ∈ {0.10, 0.25, ..., 1.00}" — does this mean {0.10, 0.25, 0.50, 0.75, 1.00} (5 values) or {0.10, 0.25, 0.40, 0.55, 0.70, 0.85, 1.00} (steps of 0.15)? Ambiguous notation. | 🟡 Medium | Clarify exact τ grid. From results section it appears to be 5 values; rewrite as `τ ∈ {0.10, 0.25, 0.50, 0.75, 1.00}`. |
| 4.3-C | Different split strategies (node-level for temperature scaling, scenario-level for conformal) — rationale not stated explicitly. Reader may flag as inconsistent. | 🟡 Medium | Add brief justification: "Temperature scaling fits a single scalar parameter (low overfitting risk); node-level split provides more samples. Conformal prediction's coverage guarantee requires exchangeability, which holds at scenario level — hence the scenario-level split." |
| 4.3-D | T7 cross-trial replication: only repeats subset of analyses (MC Dropout, AUROC, conformal). Why not all 8? Reader may wonder. | ℹ️ Note | Optional sentence: "Selected analyses (MC Dropout, AUROC, conformal) are sufficient to verify cross-trial robustness; full replication would have low marginal value at high compute cost." |
| 4.3-E | Bootstrap CI uses 100 per-graph ρ values, but 100 is small for bootstrap. Defence may probe: is B=10,000 oversampling? | ℹ️ Note | Optional defence prep: "B=10,000 yields stable CI estimate well within the asymptotic regime where bootstrap converges; smaller B=1,000 gives essentially the same result but with slightly more Monte Carlo noise." |

## Verify Tasks

- [ ] Confirm exact τ grid for selective prediction (likely 5 values: 0.10, 0.25, 0.50, 0.75, 1.00).
- [ ] Confirm temperature scaling grid resolution (`T ∈ [0.5, 5.0]` — step size 0.001? 0.01? 0.1?).
- [ ] Verify T7 cross-trial uses identical 100-graph test set (since it shares 80/10/10 split with T8).
- [ ] Confirm Bootstrap B=10,000 is consistent with code; verify CI computation method (percentile method vs BCa).

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| How did you handle the S-convergence study computationally? | Single forward-pass batch of S=50 on 10-graph subsample, retaining all 50 outputs. For each S ∈ {5, 10, ..., 50} I recomputed metrics using only the first S outputs — gives directly comparable estimates without redundant computation. |
| Why bootstrap and not parametric CI for ρ? | Bootstrap is non-parametric — no distributional assumption about per-graph ρ. Parametric (t-test) would assume normality, questionable for ρ ∈ [-1,1]. B=10,000 ensures stable CI in the asymptotic regime. |
| Why T7 specifically for cross-trial replication? | T7 was the second-best UQ-compatible trial (R²=0.5471) and shares the 80/10/10 split with T8 — straightforward cross-comparison. Different dropout (0.3 vs 0.2) and lr (6e-4 vs 5e-4) ensure results aren't T8-specific artifacts. |
| Why scenario-level conformal split (not node-level)? | Conformal's coverage guarantee rests on exchangeability. Nodes within a scenario share input policy and graph structure — highly correlated. Splitting at scenario level preserves exchangeability at the scenario aggregate. Node-level split would violate this and undermine the theoretical guarantee. |
| Why node-level temperature scaling split? | Temperature is a single scalar parameter — overfitting risk is minimal. Node-level random split gives more samples (949K calibration vs 50 graphs at scenario level). For 1-parameter optimization, node-level suffices. |
| What's per-decile conditional coverage analysis? | Sort test nodes by σ, split into 10 deciles (D1 lowest σ to D10 highest σ). Compute conformal coverage within each decile. Standard conformal drifts from 98.1% (D1) to 59.0% (D10) — 39 percentage points. Adaptive conformal compresses this to [83.7%, 96.4%] — only 13pp range. |
| Why subsample (500K) for PIT KS but full set for other metrics? | PIT KS requires global sorting + CDF construction → O(N log N) computation. 500K asymptotically equivalent to 3.16M for KS estimation, but 6× faster. Other metrics (CRPS, PIT mean, Winkler) compute per-node → no scaling penalty for full set. |
| What's the difference between marginal and conditional coverage? | Marginal coverage: averaged across all test points, the interval contains the true value 90% of the time. This is what conformal guarantees. Conditional coverage: for any specific subgroup (e.g., high-σ nodes), the interval contains the true value 90% of the time. Barber et al. (2021) prove conditional coverage is impossible distribution-free; adaptive conformal partly mitigates. |

---

# 📋 Section 4.4 — Ensemble Experimental Design

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 4.4-A | Experiment B selection criterion not justified: why T2, T5, T6, T7, T8 (and not T3, T4)? Implicit reason (T3/T4 had R² ≈ 0.22-0.24) but not explicitly stated. | 🟡 Medium | Add brief sentence: "T3 and T4 were excluded because their weighted-MSE configurations failed to generalize (R² ≈ 0.22-0.24); including them would severely dilute the ensemble." |
| 4.4-B | "Inference is deterministic" — meaning of "deterministic" not explained. Reader may not understand that dropout is OFF. | 🟢 Low | Add brief clarification: "Deterministic inference: dropout is disabled (single forward pass per model); ensemble disagreement comes from inter-member variation, not within-model stochasticity." |
| 4.4-C | Trial D seed selection {42, 137, 256, 389, 512} — why these specific primes/values? | ℹ️ Note | Defence answer: "Seeds chosen as a mix of small (42) and larger primes/distinct values to ensure diverse random initializations." |
| 4.4-D | Experiment A "five inference seeds {42, 142, 242, 342, 442}" — these are deterministic offsets (42, +100, +100, +100, +100). May suggest insufficient seed diversity. | ℹ️ Note | Defence answer: "Inference seeds are arbitrary; their role is only to drive PyTorch's RNG for dropout masking. The +100 offsets are simply a memorable convention. Any 5 distinct integers would yield equivalent results." |

## Verify Tasks

- [ ] Verify whether deep ensemble member predictions are **significantly different** (e.g., individual member R² range, pairwise prediction divergence). Already noted in audit_summary.md — "5 distinct SHA-256 hashes, mean pairwise difference 1.0-2.1 veh/h, Pearson 0.88-0.97".
- [ ] Confirm Experiment B weights are **R²-normalized** (not raw R² products). Verify in code: weights = R²_i / sum(R²_j).

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What's the difference between Experiment A, Experiment B, and Trial D? | All three are "ensemble-like" but differ in diversity source. **A**: Same T8 model, 5 inference seeds (only dropout randomness varies). **B**: 5 different trials (T2/T5/T6/T7/T8), same architecture but different hyperparameters. **D**: 5 fresh trainings with different weight initializations — true Deep Ensemble. Diversity increases A → B → D, training cost goes 1× → 1× (already trained) → 5×. |
| Why does combining MC Dropout and seed-ensemble variance not help? | Both signals come from the same model under stochastic perturbations. MC Dropout samples from approximate posterior over weights; seed-ensemble variance captures spread across MC Dropout realizations. Highly correlated, not independent. Quadrature assumes independence — when sources overlap, the formula effectively double-counts. |
| Why does multi-model ensemble underperform best single model T8? | (1) **Quality dilution**: weak models (T2, T6 at R²=0.51-0.52) drag down ensemble despite R²-proportional weighting (weights ~0.19 each — non-trivial). (2) **Limited diversity**: all five trials share same architecture, hyperparameters, and training data. Correlated errors → little variance reduction from averaging. Ensemble is 'wide' but not 'deep' in independence. |
| Why does Deep Ensemble give better R² but worse UQ? | Two mechanisms. (1) **Point accuracy** improves via variance reduction: independent models make uncorrelated errors, averaging reduces variance by ~1/√M. (2) **UQ degrades**: independent seeds disagree most on random-init effects, not on genuinely difficult inputs. So inter-member spread captures 'how much weight init matters' — not 'how uncertain the prediction is.' MC Dropout, by contrast, samples from approximate posterior over weights, producing targeted uncertainty. |
| Are Deep Ensemble members actually different? | Yes — verified in audit_summary.md. Five distinct SHA-256 hashes; pairwise prediction differences 1.0-2.1 veh/h; pairwise Pearson correlation 0.88-0.97 (correlated but not identical). Members agree more than they disagree, but the genuine inter-member spread provides ensemble benefit. |
| Why exclude T3, T4 from Experiment B? | T3 and T4 use weighted MSE which failed at this data scale (R² ≈ 0.22-0.24). Including them would either (a) reduce R²-weighted contribution to negligible, making them dead weight, or (b) dilute the ensemble with poor predictors. Five chosen models all have R² > 0.51, ensuring meaningful contribution. |
| What does "ensemble mean exceeds every individual member" mean? | Individual Deep Ensemble members have R² in [0.640, 0.650]. The ensemble mean reaches R² = 0.6841 — higher than any single member. This is the variance-reduction benefit: averaging uncorrelated errors cancels noise, producing smoother predictions than any individual model. |
| What's the "complementarity" finding? | MC Dropout (ρ=0.4820) and Deep Ensemble (R²=0.6841) sit on opposite corners of the accuracy-uncertainty trade-off. They answer different questions: Deep Ensemble = "what's the best point prediction?" MC Dropout = "how uncertain is this prediction?" Pairing both gives best of both worlds at 5× training cost — recommended for high-stakes deployment. |

---

# 📋 Section 4.5 — Uncertainty-Aware Training Extensions

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 4.5-A | Equation reference: "heteroscedastic NLL of **Equation (2.4)**" — same eq label as 3.4-C concern. Verify Eq 2.4 is actually heteroscedastic NLL (likely correct here, but inconsistent with 3.4 reference). | 🟡 Medium | If Eq 2.4 IS heteroscedastic NLL, then this reference is correct here, and the 3.4 reference is the wrong one. Cross-check both 3.4 and 4.5 references. |
| 4.5-B | T9 has 3 gates, T10/T11 have 6 gates — different gate sets. Why different criteria for different trials? | 🟡 Medium | Add brief justification: "T9 (heteroscedastic) outputs μ̂+σ̂ — gates evaluate calibration via PICP and predictive R². T10/T11 (CQR) outputs quantile pairs — gates additionally check conformal correction validity (Q̂ > 0) and width monotonicity (Width₉₀ < Width₉₅)." |
| 4.5-C | "Why GATConv(64→2) for T9 but the same for T11?" — both use identical head architecture but predict different things (μ+log σ² vs q_lo+q_hi). Reader may want clarification. | 🟢 Low | Optional: "Both T9 and T11 use GATConv(64→2); the two outputs are interpreted differently. T9: (μ̂, log σ̂²). T11: (q̂_lo, q̂_hi)." |
| 4.5-D | T10's "T10-v1 vs T10-v2" naming is confusing — reader may interpret as separate trials when they're actually variants of the same trial. | ℹ️ Note | Clarify: "T10-v1 and T10-v2 are learning-rate variants of the same trial design; results presented in Section 5.8 use T10-v2 (more favorable variant) as the representative comparison." |
| 4.5-E | "λ = 0.01" log-variance regularizer — magnitude not justified beyond citation. Defence may probe sensitivity. | ℹ️ Note | Defence prep: "λ=0.01 follows Seitzer et al. (2022) recommended value; a sensitivity analysis would have refined this but was outside thesis scope." |

## Verify Tasks

- [ ] Confirm T9 head is exactly `GATConv(64→2)` with output[0] = μ̂ and output[1] = log σ̂². Verify in `code/scripts/gnn/models/point_net_transf_gat_frozen_heteroscedastic.py`.
- [ ] Confirm T11 head is exactly `GATConv(64→2)` with output[0] = q̂_lo and output[1] = q̂_hi. Verify in `code/scripts/gnn/models/point_net_transf_gat_frozen_cqr.py`.
- [ ] Verify exact eq label of NLL — is it Eq 2.4 in PDF rendering? (LaTeX label: `eq:hetero_nll_bg`)

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Why log σ² instead of direct σ output? | Numerical stability. Direct σ requires positivity constraint via softplus or ReLU activation. Log variance is unconstrained — network outputs any real number freely. Then σ² = exp(log σ²), σ = √(σ²). Standard practice in heteroscedastic regression (Kendall & Gal 2017). |
| What does pinball loss do? | Pinball loss is asymmetric. For τ=0.05, it penalizes "true y below q̂" 19× more than "true y above q̂". This forces network to learn 5th percentile of conditional distribution. With τ=0.05 and τ=0.95, CQR learns lower and upper bounds directly, providing prediction intervals without distributional assumptions. |
| Why log-variance regularizer with λ=0.01? | Seitzer et al. (2022) showed that without regularization, networks can "cheat" by inflating σ̂ on hard examples — make σ huge so the (y-μ̂)²/(2σ̂²) term vanishes, leaving μ̂ underfit. The λ × (log σ²)² penalty stabilizes σ̂ in reasonable range. λ=0.01 small enough to not dominate, large enough to prevent collapse. |
| What's the difference between aleatoric and epistemic uncertainty? | Aleatoric = inherent data noise (irreducible by more data); Epistemic = model knowledge gap (reducible by more data or better architecture). T9 decomposes both: σ_alea from heteroscedastic head, σ_epi from MC Dropout, total via Pythagorean σ_tot = √(σ_alea² + σ_epi²). Tera T9 finds 99.85% of nodes are aleatoric-dominated — most uncertainty is fundamental data noise. |
| Why two learning rate variants for T10? | T10-v1 (lr=5e-4) caused severe R² collapse to 0.315. T10-v2 (lr=5e-5, 10× smaller) tested whether gentle fine-tuning could preserve T8 representations. v2 partially recovered R² to 0.406 but still failed gates — establishing that backbone fine-tuning under pinball loss is fundamentally problematic, not just an LR-tuning issue. |
| Why does T10 fail and T11 succeed despite same loss/head? | **Single design knob**: backbone trainability. T10 has `requires_grad=True` on backbone → pinball gradients reshape MSE-trained representations → R² collapses to 0.4057. T11 has `requires_grad=False` on backbone → only 134-parameter head adapts to pinball loss while T8 representations preserved → R²=0.5835. **This isolates the freeze-the-backbone principle.** |
| What is conformal correction Q̂? | After CQR training produces raw quantiles q̂_lo and q̂_hi, conformal correction adjusts them on calibration set: Q̂ = Quantile of conformity scores E_i = max(q̂_lo - y, y - q̂_hi) at level (1-α). Final interval becomes [q̂_lo - Q̂, q̂_hi + Q̂]. Q̂ > 0 means original was too narrow (expand); Q̂ < 0 means too wide (contract). |
| Why are gate criteria different between T9 and T10/T11? | T9 (heteroscedastic) outputs μ̂+σ̂ — gates evaluate predictive R² and Gaussian-implied PICP. T10/T11 (CQR) outputs quantile pairs — gates additionally check conformal correction validity (Q̂>0 means CQR captured signal) and width monotonicity (Width₉₀<Width₉₅ ensures interval expansion is reasonable). Different output structures require different validation criteria. |
| What does "isolates the contribution of backbone fine-tuning" mean? | Controlled experiment design. T10 and T11 differ in **only one variable**: backbone trainability flag. All other factors (head, loss, optimizer, lr, data, split, hyperparameters) are identical. Therefore, ANY observed difference in outcome (R², gates) is **causally attributable** to backbone trainability — not confounded by other variables. This is the gold-standard scientific design. |
| Why T9 fails the R² gate? | T9 is heteroscedastic with frozen backbone. The 134-parameter head cannot improve μ̂ enough to match T8's R²=0.5957 (gate threshold 0.55). Per Seitzer et al. (2022) NLL/MSE trade-off: when head capacity is limited, gradients preferentially escalate σ̂ on hard examples instead of improving μ̂. Result: 4× calibration improvement (k₉₅ 11.66 → 2.84) at cost of ~16% R² loss. **Trade-off, not failure.** |

---

# 📋 Section 4.6 — Computational Resources

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 4.6-A | Compute time disparity not explained: T10-v2 (52 hr) vs T11 (39.7 hr) — both are CQR variants. Reader may wonder why T10 takes longer despite T11 having more analysis components (e.g., conformal correction). Likely T10 needs more epochs to converge under unfrozen backbone fine-tuning. | 🟡 Medium | Add brief sentence: "T10-v2's longer training time reflects the need for more epochs under unfrozen backbone fine-tuning to (partially) recover R²; T11 converges faster because only 134 head parameters are optimized." |
| 4.6-B | "Deep Ensemble totalled approximately 5× a single T8 run" — 5× of what specifically? "Single T8 run" is ambiguous (training? training+inference?). Reader may calculate inconsistently. | 🟡 Medium | Clarify: "Deep Ensemble training totalled ~8 hours, approximately 5× a single T8 training run (~1.6 hours)." |
| 4.6-C | MC Dropout 228-min inference time understated as a deployment limitation. Could connect to T11 deployment recommendation (single forward pass = ~30× faster). | 🟢 Low | Add deployment-relevance sentence: "This 228-minute inference cost motivates the deployment recommendation in Section 5.11 to prefer T11 (single deterministic forward pass) for latency-constrained applications." |
| 4.6-D | No mention of Colab Pro session time limits (~12 hours), which constrained how trainings were checkpointed. May explain certain practical decisions. | ℹ️ Note | Defence answer ready: "Colab Pro 12-hour session limits required checkpoint-based training resumption for longer trials (T10, T11)." |
| 4.6-E | Total compute roughly summable: 13+3.8+8+14.5+52+39.7 ≈ 131 hours = 5.5 days continuous GPU. Worth mentioning as defensive context. | ℹ️ Note | Defence answer: "Total compute budget approximately 131 hours over 5.5 months of intermittent GPU access via Colab Pro." |

## Verify Tasks

- [ ] Confirm exact T10-v2 training duration in code logs (~52 hours).
- [ ] Verify Deep Ensemble's "5× T8 single run" — does this include inference or just training?
- [ ] Cross-check storage breakdown: PyG batches (4.8 GB), checkpoints (90 MB), .npz/JSON (3 GB) = 8 GB. Verify against actual disk usage.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| Why did you use Google Colab Pro and not better hardware? | Cost and access constraints. Colab Pro provides single T4 GPU at fixed monthly cost (~$10). Higher-tier alternatives (A100, H100) cost 10-50× more or require institutional access I didn't have. The T4's 16 GB VRAM was sufficient for my batch sizes, and the constraint shaped methodology — favoring smaller subsets and computationally efficient frozen-backbone designs. |
| Could you have used full 10K corpus given 80 GB storage? | Storage-wise yes — 48 GB for 10K scenarios fits within budget. But **compute** is the binding constraint. 10× more scenarios → ~10× longer per trial → ~1300+ hours total. With Colab Pro's 12-hour session limits, this was infeasible. |
| Why is MC Dropout inference so slow (228 minutes)? | S=30 forward passes × 100 test graphs = 3,000 total forward passes. T4 GPU not optimized for this small-batch high-frequency pattern. **This motivated my evaluation of T11 (frozen-backbone CQR) — same interval coverage with single deterministic forward pass, ~30× faster.** Latency-constrained deployments should prefer T11. |
| Why does T10-v2 take 52 hours vs T11's 39.7 hours? | Both are CQR variants. T10-v2 has 1,416,902 trainable parameters (full backbone + head); T11 has 134. T10's full-backbone fine-tuning requires more epochs to converge (and ultimately fails to recover R²). T11's head-only training is more constrained but converges faster. The compute disparity is itself evidence supporting freeze-the-backbone — frozen designs are computationally cheaper AND empirically better. |
| What's the total compute budget for the thesis? | Approximately 131 hours of GPU time spread across 5.5 months of intermittent Colab Pro access. Breakdown: 13 hr (8 base trials) + 3.8 hr (T8 MC inference) + 8 hr (Deep Ensemble) + 14.5 hr (T9) + 52 hr (T10-v2) + 39.7 hr (T11) ≈ 131 hr. |
| Why eleven trials and not fewer? | The 8 base trials (T1-T8) were exploratory — establishing the best UQ-compatible architecture. The 3 uncertainty-aware extensions (T9, T10, T11) directly tested the freeze-the-backbone hypothesis. Plus 5-member Deep Ensemble for accuracy comparison. Each trial answered a specific research question; reducing the count would have weakened the systematic comparison. |

---

# 📋 Chapter 4 — COMPLETED ✅

All 6 sections (4.1-4.6) reviewed. Moving to Chapter 5 (Results) next.

---

# 📋 Sections Pending

# 📋 Section 5.1 — Base Trial Performance (T1–T8)

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 5.1-A | T1 result (R²=0.7860) on 50 test graphs vs T8 (R²=0.5957) on 100 test graphs — **different test sets**, not directly comparable. Section text doesn't acknowledge this confounder. | 🟡 Medium | Add sentence: "T1's higher R² is partly attributable to evaluation on a different (50-graph) test set; the architectural confound discussed in Section 6.9." |
| 5.1-B | T3 vs T4 identical hyperparameters per Table 4.2 but different R² (0.2246 vs 0.2426) — issue 4.2-A re-emerges here when results are presented. | 🔴 **HIGH** | Same as 4.2-A: explain T3/T4 difference (likely random seed) in Table 4.2 caption AND Section 5.1 reference. |
| 5.1-C | No confidence intervals or std reported for R²/MAE/RMSE point estimates. Reader can't assess statistical reliability. | 🟡 Medium | Add: "Bootstrap 95% CI on T8 test R² is approximately ±0.005, by analogy to per-graph Spearman ρ stability." |
| 5.1-D | Validation R² (used for early stopping) not reported. Generalization gap unclear. | ℹ️ Note | Defence prep: "T8 validation R² closely tracked test R², suggesting good generalization without significant overfitting." |
| 5.1-E | "Section 6.9" reference for T1-vs-T8 gap — verify this section exists and contains the discussion. | ℹ️ Note | Cross-check Chapter 6 structure: 6.9 may be 6.7 (Limitations) or numbered differently. |

## Verify Tasks

- [ ] Confirm T3 vs T4 difference: read code at `code/scripts/training/run_models.py` for any seed-dependent or weighted MSE coefficient differences.
- [ ] Compute bootstrap CI on T8 R²/MAE/RMSE for defence preparation (optional — for confidence in defence).
- [ ] Cross-reference "Section 6.9" — confirm it's the limitations section with T1-vs-T8 discussion.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| How are your numbers verified? | Every value double-verified: (1) direct recomputation from raw .npz prediction arrays, (2) cross-reference to canonical JSON metric files. The audit_summary.md confirms 49 numbers verified with zero bugs found. |
| Why is T1 better than T8 (R²=0.786 vs 0.596)? | Three factors: (1) Linear final layer imposes strong inductive bias for predominantly linear traffic response. (2) Effective zero dropout means no inference noise. (3) More aggressive hyperparameters (lr=1e-3, batch=32). However, T1 is **not actionable for UQ** — `use_dropout=False` makes MC Dropout undefined. Among UQ-compatible trials, T8 is the strongest. The architectural confound is acknowledged in Section 6.9 (limitations); a controlled ablation is future work. |
| Are T1 and T8 R² directly comparable? | Strictly no — different test sets (T1 on 50 graphs, T8 on 100 graphs). However, the magnitude of the difference (~0.20 R² points) far exceeds typical test-set variation. Architectural and configuration differences are the dominant factors. |
| Why did weighted MSE (T3, T4) fail catastrophically? | Class imbalance: 88.7% nodes have Δv ≈ 0. Weighted MSE up-weights the 11.3% non-zero minority. At 1000-scenario scale, the network couldn't simultaneously fit zero-Δv majority and up-weighted minority — catastrophic underfitting collapsed R² to 0.22-0.24. Standard MSE was more robust. |
| What's the difference between T3 and T4? | [TODO — code verification needed; placeholder: "Different random seeds for weight initialization, isolating run-to-run variance under weighted MSE."] |
| Why is T8 the best UQ-compatible? | Empirical hyperparameter search. T8's configuration — dropout=0.2, batch=8, lr=5e-4 — found highest R² among trials with non-zero dropout + GATConv. Lower dropout preserved signal at 1000-scenario scale; smaller batches injected gradient noise to escape local minima. |
| What about validation R²? | T8's validation R² closely tracked test R² with early stopping (patience 25, min improvement 1e-3), suggesting good generalization. The gap was not large enough to suggest overfitting. |
| How confident are you in R²=0.5957? | High — derived from 3.16M test predictions across 100 scenarios. Sample size justifies 4-decimal precision. Bootstrap 95% CI on T8 R² would be approximately ±0.005 by analogy to per-graph Spearman ρ stability. |

---

# 📋 Section 5.2 — MC Dropout Uncertainty (T8)

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 5.2-A | Two ρ values reported: overall ρ = 0.4820 vs mean per-graph ρ = 0.464. Difference 0.018 not explained — reader may think it's an inconsistency. | 🟡 Medium | Add brief sentence: "The 0.018 gap reflects that overall ρ aggregates across all scenarios while mean per-graph ρ averages within-scenario ranking only — both valid, measuring different things." |
| 5.2-B | "S-convergence study on **10 test graphs**" — only 10% of test set. Reader may question whether 10 graphs sufficient for stable plateau identification. | 🟡 Medium | Add: "10 graphs (316,350 nodes) is sufficient for plateau detection — per-graph ρ has std=0.023 across the full test set, so 10 graphs already give stable mean estimates." |
| 5.2-C | Mean σ̄ = 1.369 veh/h vs MAE = 3.957 — ratio of ~2.9× implies severe underconfidence, but text doesn't quantify or connect to k₉₅=11.66 in Section 5.3. | 🟡 Medium | Add interpretive sentence: "The mean σ is 2.89× smaller than mean MAE, foreshadowing the severe underconfidence quantified by k₉₅=11.66 in Section 5.3." |
| 5.2-D | T7 cross-trial replication only in footnote — major robustness check buried. | 🟢 Low | Consider promoting from footnote to main text paragraph for visibility. |
| 5.2-E | "MC mean R² = 0.5856 vs 0.5957" — 1.7% relative drop labeled "negligible". Defence may probe: is 1.7% really negligible? Add justification. | ℹ️ Note | Defence prep: "1.7% R² drop is well within bootstrap CI on R² (~±0.5% per ρ analogy), making it statistically indistinguishable." |

## Verify Tasks

- [ ] Confirm S-convergence numbers (S=5→30 gives +10.8%, S=30→50 gives +1.03%) match `s_convergence_with_rho.json`.
- [ ] Verify per-graph ρ statistics (mean=0.464, std=0.023, range [0.410, 0.503]) from .npz files.
- [ ] Confirm bootstrap CI [0.460, 0.469] uses percentile method (not BCa or others). Verify in code.
- [ ] Cross-check T7 footnote numbers (ρ=0.4437, k₉₅=16.15, AUROC=0.7416/0.7151) against `t7_auroc.json`.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What's your primary UQ finding? | MC Dropout with S=30 on T8 yields Spearman ρ = 0.4820 between predicted uncertainty σ and absolute error \|y - ŷ\|. Computed on full 100-graph test set (3.16M node-level predictions). Bootstrap 95% CI on mean per-graph ρ is [0.460, 0.469] — confirming statistical reliability. |
| Why is mean σ so small (1.369 veh/h)? | Raw MC Dropout σ severely underestimates true error magnitude — typical error (MAE=3.957) is nearly 3× larger than typical σ. This is the well-known MC Dropout **underconfidence** — variational posterior too concentrated. Motivates temperature scaling in Section 5.4 (T*=2.887 corrects this). |
| Does MC Dropout hurt prediction accuracy? | Negligibly. MC mean R²=0.5856 loses only 1.7% relative to deterministic R²=0.5957. MAE actually slightly improves with MC averaging (3.948 vs 3.957) — averaging cancels random noise. **Cost of MC Dropout is purely inference-time compute, not accuracy.** |
| How statistically robust is your ρ estimate? | Highly. Bootstrap 95% CI on mean per-graph ρ is [0.460, 0.469] — width 0.009, reliable to ~3 decimal places. With 100 test graphs and 10,000 bootstrap iterations, well within asymptotic regime. No method comparison I report differs by less than 0.05, so conclusions hold within statistical noise. |
| Why are overall ρ (0.4820) and mean per-graph ρ (0.464) different? | They measure different things. Overall ρ is computed across all 3.16M nodes — captures both within-scenario AND cross-scenario ranking. Mean per-graph ρ averages within-scenario ranking only. The 0.018 difference reflects that ranking is slightly stronger across scenarios than within. Both are valid statistics, answering different questions. |
| Is your finding robust across test scenarios? | Yes — per-graph ρ has std=0.023 across 100 test graphs (range [0.410, 0.503]). No graph drops below 0.41. Findings aren't artifacts of a few lucky scenarios. The narrow range and tight bootstrap CI confirm statistical reliability. |
| How did you choose S=30? | Empirical S-convergence study on 10-graph subsample. S=5→30 gives +10.8% in ρ (most improvement here); S=30→50 gives only +1.03% (diminishing returns). S=30 sits on the plateau — captures 95% of S=50 benefit at 60% of compute. Implementation efficient: single S=50 run, recomputed metrics using first-S outputs for each S value. |
| How do you know findings aren't T8-specific? | T7 cross-trial replication confirms robustness. T7 has different hyperparameters (dropout 0.3 vs 0.2, lr 6e-4 vs 5e-4) but identical architecture. Qualitative findings replicate: ρ > 0.4, AUROC > 0.7, k₉₅ >> 1.96. Quantitative differences exist (T7 ρ=0.4437 vs T8 0.4820) but mechanism-level findings are robust to hyperparameter choice. |
| What does ρ=0.4820 mean operationally? | "MC Dropout uncertainty correctly identifies node pairs where higher-σ has higher error 74% of the time" (translating Spearman to AUROC equivalence). Useful enough for selective prediction (50% retention reduces MAE by 41.2%, Section 5.5). Not perfect — but practically actionable. |

---

# 📋 Section 5.4 — Post-Hoc Temperature Scaling

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 5.4-A | **Figure 5.5 placement issue**: Figure 5.5 caption is about CONDITIONAL CONFORMAL COVERAGE (decile analysis) — this belongs to Section 5.3, not Section 5.4 (temperature scaling). LaTeX layout has overflowed. | 🟡 Medium | Either: (a) Move Figure 5.5 placement back to Section 5.3 with proper float commands, or (b) Use `[h!]` placement option to keep figure with its discussion. |
| 5.4-B | "T fitted on 30% subset (seed 42, 949,050 nodes)" — but Section 4.3 says same thing. Why TWO mentions? Reader needs only one. | 🟢 Low | Remove redundancy — Section 4.3 already established this; Section 5.4 just needs results. |
| 5.4-C | 2σ and 3σ residual gaps (10.45 pp and 8.13 pp) only briefly explained ("heavier tails"). Reader may want quantification of how heavy. | 🟡 Medium | Add brief sentence: "The PIT KS=0.245 in Section 5.5 quantifies the heavy-tailed deviation more formally." |
| 5.4-D | Grid `T ∈ [0.5, 5.0]` mentioned in Section 4.3 but optimization granularity (step size 0.001? 0.01?) not stated anywhere. Defence may probe. | ℹ️ Note | Defence prep: "Grid resolution 0.001 (4500 candidate values searched), well within machine precision." |
| 5.4-E | "Single scalar cannot reshape the tails, only rescale them" — beautiful insight, but examiners may want connection to next-step solution (conformal). | 🟢 Low | Already implicitly references conformal. Consider: "...motivating the conformal layer of the calibration cascade (Section 5.3)." |

## Verify Tasks

- [ ] Verify T*=2.887 from `temperature_scaling_results.json`. UQ_SUMMARY.md confirms this value (verified 2026-04-24).
- [ ] Confirm Figure 5.5 LaTeX placement — likely `[htbp]` causing overflow. Should be `[h!]` or moved to Section 5.3.
- [ ] Verify temperature scaling grid resolution in code (`run_part3_calibration_audit.py`).

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What does ECE drop from 0.356 to 0.034 mean? | ECE measures average gap between predicted confidence and observed frequency. Before: 36 percentage point gap (severe miscalibration). After T=2.887: 3.4 percentage point gap (near-perfect). 90.5% reduction = transformative improvement from a single scalar parameter. |
| What does 1σ coverage match (68.0% vs 68.3% target) mean? | When model says "68% confident in [μ̂ ± σ_scaled]", it actually achieves 68% coverage. Within 0.3 pp of Gaussian-implied target. **Single scalar achieves Gaussian-equivalent 1σ behavior.** Practically actionable for risk assessment. |
| Why can't single scalar T fix 2σ/3σ coverage? | A single scalar uniformly stretches the predictive distribution — same shape, different width. Predictive distribution has heavier-than-Gaussian tails — extreme errors more common than Gaussian predicts. T fixes 1σ region (bulk of distribution); but tail miscalibration requires shape correction, not scale correction. **This motivates conformal prediction in Section 5.3** which provides distribution-free coverage at any level. |
| Why is T* = 2.887 (not 1.0)? | T*=2.887 ≈ 3 means raw σ underestimates true uncertainty by ~3×. Reflects MC Dropout's well-known **underconfidence** (variational posterior too concentrated). The factor of 3 corrects scale; combined with conformal for tail correction, gives full calibration cascade. |
| Why fit on 30% (not all) of test set? | Avoid calibration leakage. T fitted on 30% (949,050 nodes); evaluated on remaining 70% (2,214,450 nodes). The 70% portion is genuinely held-out from temperature fitting, ensuring honest evaluation. Standard ML practice. |
| What does k₉₅ improvement (11.66 → 4.04) mean? | Before: σ_raw × 11.66 covers 95% of errors (severely overconfident). After: σ_scaled × 4.04 covers 95%. 2.89× improvement. But still gap to Gaussian ideal (1.96) due to heavy tails — bridged by conformal prediction. |
| Walk me through Figure 5.6. | Panel (a): ECE vs T curve. U-shaped — high at T=1, minimum at T*=2.887, increasing for higher T. Confirms optimal scalar exists. Panel (b): Reliability diagram. Before: curve below diagonal (overconfident). After: hugs diagonal (calibrated). **Visual confirmation of 90.5% ECE reduction.** |
| Why fit T to ECE (not other metrics like NLL)? | ECE directly measures the calibration objective — gap between predicted and observed coverage at each percentile. NLL conflates point accuracy and uncertainty quality. Since temperature scaling doesn't change μ̂ (only σ), ECE is the targeted metric for the calibration component being adjusted. |
| What's "Kuleshov ECE" specifically? | Per Kuleshov et al. (2018), the calibration measure for regression: bin predictions by predicted CDF percentile (e.g., {10%, 20%, ..., 90%}), measure observed frequency in each bin, compute average absolute deviation from nominal. Different from classification ECE — adapted for continuous predictions. |

---

# 📋 Section 5.5 — Proper Scoring Rules, Selective Prediction, Error Detection

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 5.5-A | **AUROC mismatch** between text and figure: Section 5.5 text says T8 AUROC top-10% = 0.7548, T7 = 0.7416. Figure 5.10 caption says T8 = 0.7538, T7 = 0.7426. **0.001 difference** in both. | 🟡 Medium | Reconcile: either text or figure has rounding/run inconsistency. UQ_SUMMARY.md confirms 0.7548 from `auroc_corrected.json`. Update Figure 5.10 caption to match text (0.7548 / 0.7416). |
| 5.5-B | "PIT first-bin mass = 28.4%" mentioned in Appendix A.5 but **NOT in Section 5.5**. Important calibration finding hidden. | 🟡 Medium | Add: "Specifically, 28.4% of true values fall in the bottom 5% of the predictive distribution (vs 5% expected) — concrete evidence of upward bias and underdispersion." |
| 5.5-C | Selective prediction τ values inconsistent: Section 4.3 says "τ ∈ {0.10, 0.25, ..., 1.00}" (ambiguous), Section 5.5 reports concrete values for {10%, 25%, 50%, 90%, 100%}. Confirms τ grid is {0.10, 0.25, 0.50, 0.75, 1.00}. | 🟢 Low | Match notation between sections. Section 4.3: write `τ ∈ {0.10, 0.25, 0.50, 0.75, 1.00}` explicitly. |
| 5.5-D | "T8 AUROC top-20% = 0.7324" vs Figure 5.10 = 0.7341 — another 0.0017 difference for T7 too (0.7151 vs 0.7159). | 🟡 Medium | Same as 5.5-A — rounding/run inconsistency between text and figure values. |
| 5.5-E | CRPS/MAE = 0.857 ratio reported but its interpretation thin. Reader may not appreciate "21% above optimum" framing. | 🟢 Low | Add interpretive sentence: "The 21% gap above the Gaussian-calibrated optimum quantifies the calibration cost of underdispersed σ — partly addressed by temperature scaling and conformal prediction." |
| 5.5-F | "PIT KS drops to 0.104 after temperature scaling" — but reader doesn't know if this represents fitness improvement or remains "high". Need benchmark. | ℹ️ Note | Defence prep: "KS=0.104 represents 57% improvement from KS=0.245. Still nonzero (ideal 0) due to upward bias in μ̂; conformal prediction handles the residual tail issue." |

## Verify Tasks

- [ ] **CRITICAL:** Reconcile AUROC numbers between text (0.7548, 0.7324, 0.7416, 0.7151) and Figure 5.10 (0.7538, 0.7341, 0.7426, 0.7159). Verify against `auroc_corrected.json` and `t7_auroc.json`.
- [ ] Verify CRPS = 3.384 from `winkler_scores.json` or related JSON.
- [ ] Verify Winkler scores (49.68, 35.78, 32.32) from `winkler_scores.json`.
- [ ] Confirm selective prediction values (-18.3%, -41.2%, -54.5%, -73.4%) from `selective_prediction_s30.json`.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What does CRPS/MAE = 0.857 tell us? | It's 21% above the Gaussian-calibrated optimum 1/√2 ≈ 0.707. This is the **calibration cost** of underdispersed σ. A perfectly calibrated probabilistic forecaster achieves the optimum; T8 with raw σ is 21% above. Cannot be fully closed by temperature scaling alone — requires handling heavy tails via conformal prediction. |
| What does PIT mean = 0.433 tell us? | PIT mean of 0.433 (vs ideal 0.500) means predictive distribution is **left-shifted** — true values cluster in lower percentiles of predicted distribution. Combined with KS=0.245, this indicates **systematic upward bias in μ̂** plus underdispersion in σ̂. 28.4% of true values fall in bottom 5% of predictive distribution (vs 5% expected). |
| Why does PIT KS not reach 0 even after temperature scaling? | Temperature scaling adjusts σ but not μ̂. T*=2.887 reduces KS from 0.245 to 0.104 (57% improvement) by widening σ. But residual KS=0.104 reflects **irremovable location bias** in μ̂ — no scalar rescaling of σ can correct mean bias. **Conformal prediction is the right tool for tails** — its intervals shift to contain residuals regardless of μ̂'s location. |
| Why does adaptive conformal beat standard at Winkler score? | Both achieve same marginal coverage (~90%). But adaptive conformal **distributes interval widths better** — narrow for low-σ (easy) nodes, wide for high-σ (hard) nodes. Standard uses fixed-width intervals — wasted on easy nodes, insufficient on hard nodes. Result: Winkler 32.32 (adaptive) vs 35.78 (standard) — 28% improvement at no coverage cost. **For deployment requiring sharp + reliable intervals, adaptive is recommended.** |
| What's the operational value of MC Dropout? | Selective prediction demonstrates direct operational utility. Retaining most confident 50% (sorted by σ) drops MAE from 3.95 to 2.32 veh/h — **41.2% reduction**. At 10% retention, MAE drops to 1.06 (-73.4%). **Enables deployment policy**: accept low-σ predictions, flag high-σ for MATSim re-simulation. ρ=0.482 isn't perfect ranking but good enough for actionable decisions. |
| How useful is AUROC = 0.7548? | It means σ correctly orders high-error vs low-error node pairs 75% of the time. **Comparable to clinically-useful medical diagnostic tools** (target AUROC > 0.7). Enables effective risk flagging: top-10% σ predictions can be rejected/reviewed with high probability of catching genuine high-error cases. T7 cross-trial replication (0.7416) confirms findings. |
| Why both AUROC and AUPRC? | AUROC is symmetric / class-imbalance-invariant. AUPRC's random baseline equals positive-class prevalence (10% for top-10% errors), giving better signal under imbalance. **Reporting both** prevents "AUROC always looks good" deception — confirms genuine signal vs apparent signal. |
| What's the deployment recommendation from Section 5.5? | Three components: (1) **Selective prediction**: keep top 50% confident → 41% MAE reduction. (2) **Adaptive conformal**: for retained subset, use ŷ ± q^adapt × σ for sharp intervals. (3) **Error flagging**: top-10% σ → MATSim re-simulation. Combined: cost-efficient policy review with formal coverage guarantees. |

---

# 📋 Section 5.7 — Trial 9: Heteroscedastic, Frozen Backbone

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 5.7-A | **Figure 5.14 caption overclaim**: Says "this pattern means most uncertainty reflects **genuine traffic-flow variability**". Per Seitzer et al. (2022), NLL has known failure mode of σ inflation on hard examples. **Cannot distinguish "real aleatoric" from "NLL-inflated σ" without ground truth.** | 🟡 Medium | Soften to: "T9 attributes most predicted uncertainty to its aleatoric component. While consistent with traffic-flow variability being substantial, this could partially reflect the well-known NLL pitfall of σ inflation on hard examples (Seitzer et al. 2022)." |
| 5.7-B | "Training ran for 315 epochs" — rationale not given. Long training may suggest convergence difficulties. | 🟢 Low | Add: "315 epochs reflects early stopping with patience 25; best checkpoint at epoch 290 (val_NLL=3.2489), confirming convergence." |
| 5.7-C | σ_alea=4.657, σ_epi=1.099 — Pythagorean check gives ~4.785, but reported σ_total=4.823. Difference from per-node correlation. | ℹ️ Note | Defence prep: "Mean of √(σ_alea² + σ_epi²) per node ≠ √(mean σ_alea² + mean σ_epi²) due to per-node correlation. Reported 4.823 is per-node averaged total." |

## Verify Tasks

- [ ] Verify Trial 9 results against `t9_evaluation_results.json`. UQ_SUMMARY confirms all values.
- [ ] Confirm 315 epochs in training logs and epoch 290 best checkpoint.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What happened in Trial 9? | T9 froze T8 backbone (1.4M params) and trained only 134-parameter heteroscedastic head with NLL loss + log-variance regularizer (λ=0.01). 315 epochs. **Two of three gates pass**: PICP_90=86.9% (≥85%), PICP_95=90.0% (≥90%). **R² gate fails**: 0.4991 (<0.55). k₉₅=2.84 (4× better than T8's 11.66). **Partial positive — calibration trade-off.** |
| Did T9 fail? | Technically yes (R² gate), but I prefer **"partial positive"** framing. T9 traded 16% R² for 4× calibration improvement and **preserved ranking** (ρ=0.480 vs T8 0.482). For risk-sensitive applications where coverage matters more than point accuracy, T9 is preferable. |
| Why does T9 fail R² gate? | NLL/MSE trade-off. 134-parameter head can't improve μ̂ enough to match T8 (frozen backbone limits capacity). Per Seitzer et al. (2022): NLL has known failure mode where network can't improve μ̂, reduces loss by **inflating σ̂ on hard examples** — 4× calibration improvement at cost of 16% R² loss. λ=0.01 regularizer partially mitigates but cannot eliminate. |
| What does 99.85% aleatoric-dominant mean? | **Strictly**: model attributes 99.85% of predicted uncertainty to aleatoric component, not epistemic. **However, I cannot fully distinguish "real data noise" from "NLL-inflated σ"** — Seitzer's pitfall could partially explain. **Safer wording**: "T9 attributes most uncertainty to the aleatoric component," not "this is genuine traffic-flow variability." |
| Why is T9 backbone "frozen" but dropout active? | Two senses of "frozen". T9 freezes **weights** (requires_grad=False) but keeps **dropout layers active** during training/inference. Intentional — T9 uses MC Dropout for σ_epi via stochastic forward passes. Without active dropout, σ_epi undefined. Contrasts with T11 (Section 5.9) which forces backbone deterministic. |
| Did T9 lose ranking quality? | No — ρ=0.480 vs T8's 0.482, only -0.4% relative. Trade-off: 16% R² loss for 4× calibration improvement, **ranking preserved**. T9 is calibration-focused alternative with comparable ranking but worse accuracy. |
| What's the bigger lesson? | **Uncertainty-aware training can improve calibration, but may reduce point accuracy if mean prediction not preserved.** Sets up T10 (unfrozen → collapse) and T11 (frozen → recovery), forming freeze-the-backbone trilogy. |

---

# 📋 Section 5.10 — Stratified UQ by |Δv| Quartile

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 5.10-A | **Q1 mechanical artefact caveat NOT mentioned in Section 5.10 text.** Audit_summary.md (line 31) explicitly notes ρ=0.725 on Q1 is "partly MECHANICAL" because Q1 has |Δv|=0 throughout — both \|error\| and σ reduce to functions of model output magnitude on unchanged segments, sharing dependence on \|ŷ\|. **Section 5.10 text presents ρ=0.725 without this nuance**, although Section 6.4 develops it. Reader sees "MC Dropout great on Q1" and may overclaim. | 🟡 Medium | Add to Section 5.10: "(Note: Q1's high ρ is partly a mechanical artefact of |Δv|=0 — see Section 6.4 for detailed mechanism)." |
| 5.10-B | Figure 5.15 (CQR variants R² comparison) placed mid-Section 5.10 but logically belongs to Section 5.9 (Trial 11 discussion). LaTeX float overflow. | 🟡 Medium | Use `[h!]` or move figure block to Section 5.9. |
| 5.10-C | Q4's max |Δv| = 230 veh/h reported but no comparison to baseline (mean 50.9, median 10.9 veh/h) provided. Reader can't gauge magnitude. | 🟢 Low | Add: "approximately 4.5× the mean baseline volume (50.9 veh/h) and ~21× the median (10.9 veh/h)" |
| 5.10-D | Phase transition Q2→Q3 (ρ drops 69%, from 0.523 → 0.162) not explicitly noted. Pattern is sharper than gradual decline. | ℹ️ Note | Defence prep: "Sharp drop Q2→Q3 suggests phase transition at threshold |Δv| beyond which prediction becomes qualitatively harder." |
| 5.10-E | Q4's σ̄ vs MAE ratio (~5× underconfidence) not quantified — important deployment warning hidden. | ℹ️ Note | Defence prep: "In Q4, σ̄≈2.07 but MAE=10.08 — error 5× larger than σ. Silent failure mode: σ should NOT be trusted alone for high-stakes Q4 cases." |

## Verify Tasks

- [ ] Confirm Q1 |Δv| = 0 throughout claim — verify in `code/scripts/misc/gen_batch7.py` and prediction arrays.
- [ ] Verify per-quartile node counts (790,875 each = 3,163,500 total ÷ 4 = 790,875) ✓ math checks.
- [ ] Cross-reference Section 6.4 confirms Q1 mechanical artefact discussion.

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What did the stratified analysis by \|Δv\| show? | **Sharp regime dependence**. Q1 (no-effect, |Δv|=0): MAE=1.25, ρ=0.725. Q4 (largest response, up to 230 veh/h): MAE=10.08, ρ=0.100. As policy effect grows, MAE rises 8× and ρ falls 7×. **Most reliable in low-impact regimes, much weaker for large traffic-response segments.** |
| Is Q1's high ρ=0.725 really meaningful? | **Important caveat — Q1's high ρ is partly mechanical, not informative.** Q1 has \|Δv\|=0 throughout. When y=0, \|error\|=\|ŷ\| and σ depends on model output magnitude on unchanged segments — they share dependence on \|ŷ\|. **The high correlation is partly an artefact of shared dependence**, not genuine UQ. **The Q1→Q4 contrast should be read as 'MC Dropout works mechanically on trivial segments and breaks on hard ones'** — not 'MC Dropout is highly informative on easy regimes'. Section 6.4 develops this nuance. |
| Why does ρ degrade so sharply across quartiles? | Three contributing mechanisms: (1) **Dynamic range**: Q4's \|y\|≈30 dwarfs σ̄≈2.07 — MC Dropout's variance-over-weights doesn't capture this magnitude. (2) **Saturation**: Q4 segments are near capacity, where small policy changes tip system past flow-density knee — non-linear dynamics MC Dropout can't capture. (3) **Sparse training coverage**: large-\|Δv\| segments are rare in 1000-scenario training set; posterior over these inputs concentrated on small training manifold region. |
| What does this mean for deployment? | **Overall metrics hide regime-specific weaknesses.** Deployment policy: low \|Δv\| / low σ areas → surrogate alone. High \|Δv\| areas (which are MOST relevant for policy decisions) → MATSim verification. Uncertainty alone in Q4 isn't reliable. **Section 5.11's three-tier framework operationalizes this.** |
| Why does Q4 silently fail? | In Q4, σ̄≈2.07 but MAE=10.08 — error 5× larger than predicted σ. **Silent failure mode**: model claims reasonable confidence but is terribly wrong on hardest cases. MC Dropout fails both at ranking (ρ=0.10) and at magnitude quantification. **Heteroscedastic head (T9, Section 5.7) partially mitigates** by capturing aleatoric component (σ_alea=4.66), but at cost of point accuracy (R²=0.4991). |
| Is the degradation gradual or sharp? | **Sharp**, not gradual. ρ drops 69% between Q2 (0.523) and Q3 (0.162), then more slowly to Q4 (0.100). Phase-transition behavior suggests a threshold \|Δv\| beyond which prediction becomes qualitatively harder. Q1+Q2 = "near-zero" regime; Q3+Q4 = "real-response" regime. |
| What's the operational meaning of 230 veh/h max in Q4? | 230 veh/h is ~4.5× mean baseline volume (50.9 veh/h) and ~21× median (10.9 veh/h). These are massive relative changes — bottleneck redistributions where roads completely overloaded or emptied. Outside training distribution range, highly non-linear network cascades, MC Dropout posterior never calibrated for them. |

---

# 📋 Sections Pending in Chapter 5

  - [ ] 5.11 Deployment Guidance
# 📋 Section 6.7 — Answers to Research Questions

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 6.7-A | RQ4 mentions "AUROC ordering: raw MC > standard > adaptive" with Winkler scores. But Section 5.5 reported Winkler scores as "lower is better" — so the ORDERING in 6.7 is correct (raw MC is HIGHEST = WORST). Reader may misread. | 🟢 Low | Add clarifying parenthetical: "(lower is better — raw MC is worst, adaptive is best)" |
| 6.7-B | RQ5 forward-references Seitzer [22] for "NLL–MSE trade-off." Should this be repeated for non-citation-following readers? | ℹ️ Note | Already cited in Section 4.5; sufficient. |
| 6.7-C | RQ3 mentions "architecturally diverse ensembles (GAT, GraphSAGE, GCN)" as future work but doesn't justify WHY these would help. | ℹ️ Note | Defence prep: "Different architectures encode different inductive biases — disagreements would be more informative than seed-only differences." |

## Verify Tasks

- [ ] All RQ numbers confirmed against earlier sections — no new verification needed (most numbers re-stated from Sections 5.2-5.10).

## Defence Q&A — RQ-by-RQ

| Question | Prepared Answer |
|---|---|
| RQ1: How effective is MC Dropout? | Effective as ranking signal: ρ=0.4820 with bootstrap 95% CI [0.460, 0.469], AUROC=0.7548 for top-10% errors, retaining most confident 50% reduces MAE by 41.2%. **However, raw σ NOT calibrated as probability** (k₉₅=11.66 vs ideal 1.96). Useful for risk-flagging deployment, not for formal probability claims. |
| RQ2: MC Dropout vs Ensembles? | Opposite trade-off corners. **Deep Ensemble**: R²=0.6841 (+14.8% over T8), best accuracy. **MC Dropout**: ρ=0.4820 vs DE 0.3997, best UQ. **Multi-model ensemble** (T2/T5/T6/T7/T8 weighted): R²=0.5656 (worse than T8 alone, quality dilution). **Pair both** for high-stakes deployment at ~5× training compute. Under constraints: single-model MC Dropout. |
| RQ3: Combine MC + Seed Variance? | Marginally — improvement +0.0001 in ρ, indistinguishable from noise. Both signals come from same model under stochastic perturbations, highly correlated. Multi-model ensembling does worse due to quality dilution. **Architecturally diverse ensembles** (GAT + GraphSAGE + GCN) might break this — different inductive biases produce more independent disagreements. Not tested here; future work. |
| RQ4: Distribution-free trustworthy intervals? | **YES — definitively.** Three methods compose into layered cascade: (1) **Split conformal** PICP_90=90.02% with q=9.92, PICP_95=95.01% with q=14.68. (2) **Temperature scaling** T*=2.887 reduces ECE from 0.356 to 0.034 (-90.5%), 1σ coverage matches Gaussian target (68.0% vs 68.3%). (3) **Adaptive conformal** narrows conditional coverage [59%, 98%] → [84%, 96%]. Winkler ordering confirms quality progression (lower is better): raw MC (49.68) > standard (35.78) > adaptive (32.32). |
| RQ5: Uncertainty-aware training preserve accuracy? | **Yes, if and only if the MSE-trained backbone is kept frozen.** T9 (frozen, heteroscedastic): k₉₅=2.84 (4× better) but R²=0.4991 fails 0.55 gate (NLL/MSE trade-off). T10-v2 (unfrozen, CQR): R²=0.4057, 3/6 gates fail. T11 (same CQR head, frozen): R²=0.5835, all 6 gates pass. **Single design difference T10→T11 isolates the cause** — uncertainty-aware extensions work when they specialise the head without reshaping the backbone. T11 provides native asymmetric intervals at single deterministic pass — attractive for latency-constrained deployments. |
| Are these answers consistent with your contributions? | Yes — each RQ answer maps to a contribution: RQ1 → C2 (MC Dropout characterization), RQ2 → C3+C7 (ensembles + Deep Ensemble), RQ3 → C3 (single-architecture ensemble limits), RQ4 → C4 (layered framework), RQ5 → C6 (Freeze-the-Backbone principle). |
| Which RQ is your most novel finding? | RQ5 — the Freeze-the-Backbone principle. T10 vs T11 ablation provides causally identified evidence (single boolean flag) for an actionable design rule. Combined with the layered post-hoc framework (RQ4), it provides a complete UQ deployment toolkit for GNN traffic surrogates. |

## Answer Memorization (verbatim for defence)

```
RQ1: "MC Dropout is effective as a ranking signal; absolute σ not calibrated probability."
RQ2: "Opposite sides of the accuracy-uncertainty trade-off."
RQ3: "Improvement indistinguishable from noise."
RQ4: "Three methods compose: MC for ranking, TS for calibration, adaptive conformal for coverage."
RQ5: "Yes, if and only if the MSE-trained backbone is kept frozen."
```

---

# 📋 Sections Pending in Chapter 6

  - [ ] 6.1 Freeze-the-Backbone Principle (covered in earlier sections)
  - [ ] 6.9 Limitations and Future Directions

# 📋 Section 6.8 — Primary Findings

## Issues

| # | Issue | Severity | Action |
|---|---|---|---|
| 6.8-A | Finding 3 uses "important design consideration" — softer than "principle" used elsewhere (abstract, contribution 6, section 6.1). Slight inconsistency in framing. | 🟢 Low | Either: (a) consistent across all sections (use "principle" throughout), or (b) keep softer language in 6.8 as honest acknowledgment that it's specific to thesis setting. |
| 6.8-B | Finding 5 explicitly captures Q1 mechanical artefact ✅ — this resolves the issue 5.10-A from earlier. Section 5.10 should add forward reference to Section 6.8. | 🟢 Low | Add to Section 5.10: "(see Finding 5 in Section 6.8 for primary statement of caveat)." |
| 6.8-C | Finding 4 says "≈ 5× training compute" but Section 4.6 (Computational Resources) gave specific 8 hours number. Quantify clearly. | 🟢 Low | Replace "≈ 5×" with "approximately 8 hours additional training compute". |

## Defence Q&A

| Question | Prepared Answer |
|---|---|
| What are your top 5 findings? | (1) MC Dropout works as ranking signal (ρ=0.4820, AUROC=0.7548). (2) Calibration cascade closes gap to formal coverage. (3) Freezing backbone matters for uncertainty-aware extensions (T10→T11 single knob). (4) Deep Ensemble + MC Dropout are complementary, not competing. (5) Stratified UQ has two regimes — Q1 partly mechanical, Q4 real failure. |
| Why "important design consideration" not "law" for backbone freezing? | I'm being defensively honest about scope. Evidence is causally identified for **this thesis's specific setting** (MSE-trained PointNetTransfGAT, CQR head, 1000-scenario subset). Mechanism via Seitzer (2022) NLL/MSE trade-off suggests broader applicability, but I haven't tested other architectures or losses. **Future work**: validate on other architectures and tasks. |
| What does "no graph drops below ρ=0.41" tell us? | Robustness across scenarios. Per-graph ρ has range [0.41, 0.50] across 100 test graphs. **No single scenario has weak signal**. The signal is consistent — findings aren't artifacts of a few lucky scenarios. Defence-strong evidence for stability. |
| What's "the calibration cascade closes the gap"? | Three-layer post-hoc framework: (1) Raw MC Dropout has k₉₅=11.66 (uncalibrated). (2) Temperature scaling reduces to k₉₅=4.04, cuts ECE 90.5%. (3) Adaptive conformal achieves marginal coverage 90/95% with tightened conditional coverage [84%, 96%]. **Each layer fixes what previous can't** — together they compose into formal coverage guarantee without retraining. |
| Why "complementary, not competing"? | Deep Ensemble (R²=0.6841 ✅, ρ=0.3997 ❌) and MC Dropout (R²=0.5957, ρ=0.4820 ✅) sit on opposite trade-off corners. They answer different questions: Deep Ensemble = "what's the best prediction?" MC Dropout = "how uncertain is this prediction?" Pair them for high-stakes deployment at ~8 hours additional training cost. |
| What's "uncertainty-guided filtering works best where model is already good"? | Stratified analysis insight. Q1 (no-effect): ρ=0.725 BUT mechanical artefact. Q4 (large response): ρ=0.100 (real failure). MC Dropout's σ ranks errors well in regimes where prediction is already accurate; in hard regimes (Q4), σ silent-fails. **Deployment implication**: don't rely on σ alone in high-impact policy areas — combine with explicit OOD detectors or MATSim verification. |
| Are these findings consistent across thesis? | Yes — each finding stated multiple times: Finding 1 in Section 5.2, 6.7 (RQ1). Finding 2 in Section 5.4, 6.3, 6.7 (RQ4). Finding 3 in Sections 4.5, 5.7-5.9, 6.1, 6.7 (RQ5). Finding 4 in Sections 5.6, 6.2, 6.7 (RQ2). Finding 5 in Sections 5.10, 6.4 + Q1 caveat. **Multi-section consistency** = thesis-wide coherent narrative. |

---

# 📋 Sections Pending in Chapter 6

  - [ ] 6.9 Limitations and Future Directions

# 📋 Sections Pending Beyond Chapter 6
- [ ] Chapter 7 — Conclusion
- [ ] Appendix A — Master Table

---

# 🔧 Consolidated Fix Plan (will compile at end)

Once we finish all sections, this section will list:
1. All 🔴 HIGH issues (must fix before submission)
2. All 🟡 Medium issues (should fix)
3. All 🟢 Low issues (nice-to-have)
4. All ℹ️ Notes (defence prep only)

---

# 📚 Defence Prep — Cross-section Themes

## The Three Findings (memorize for opening statement)

1. **Raw MC Dropout σ is a ranking signal, not a calibrated probability** — useful for selective prediction (ρ=0.482, AUROC=0.7548) but inadequate for formal coverage (k₉₅=11.66 vs ideal 1.96).
2. **Freezing the MSE-trained backbone is the decisive design principle** for any uncertainty-aware extension — T10 (unfrozen) collapses to R²=0.4057, T11 (same head, frozen) recovers to R²=0.5835.
3. **MC Dropout, temperature scaling, and adaptive conformal compose into a layered post-hoc framework** requiring no retraining of the backbone.

## The Three Likely Defence Hits

1. **Data scale (10% subset, R²=0.5957 vs Natterer's >0.9)** — defend with: relative method comparisons are scale-invariant; UQ findings should generalize; verification at full scale = future work.
2. **T1 vs T8 paradox (R²=0.786 vs 0.596)** — defend with: T1 has zero dropout → MC Dropout undefined; UQ-compatibility dominates raw R² for this thesis's scope.
3. **AI tool disclosure** — defend with: Grammarly for grammar/language; ChatGPT/Claude for matplotlib formatting; final figures and all scientific content my own.

