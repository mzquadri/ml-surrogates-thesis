# Uncertainty Quantification for Machine Learning Models in Transportation Policy Analysis

**Master's Thesis** | Technical University of Munich | School of Computation, Information and Technology

|                |                                                                      |
| -------------- | -------------------------------------------------------------------- |
| **Author**     | Mohd Zamin Quadri                                                    |
| **Programme**  | M.Sc. Mathematics in Science and Engineering                         |
| **Department** | Computer Science (Data Analytics and Machine Learning)               |
| **Examiner**   | Prof. Dr. Stephan Günnemann                                          |
| **Supervisors**| Dominik Fuchsgruber, M.Sc., Elena Natterer, M.Sc.                    |
| **Submitted**  | May 15, 2026                                                         |

**[Read the thesis (PDF)](document/main.pdf)**

---

## Abstract

Agent-based simulators such as MATSim are the standard tool for evaluating urban transport policy but take hours per Paris-scale scenario; Graph Neural Network (GNN) surrogates close that gap to seconds. Accuracy alone is not enough for decision support, however, because predictions can degrade outside the training distribution without any external signal.

This thesis evaluates uncertainty quantification (UQ) for a PointNetTransfGAT GNN traffic surrogate on the Paris road network (31,635 road segments), using a fixed **1,000-scenario subset** of the 10,000-scenario MATSim corpus of Natterer et al. (2025), reused across all eleven trials. It combines post-hoc methods — MC Dropout, regression σ-scaling, split/adaptive conformal prediction, selective prediction, error detection — with three uncertainty-aware training extensions (heteroscedastic and CQR heads) to study when per-prediction uncertainty can be trusted for policy support.

---

## Key Results (as submitted, May 2026)

All values recomputed from the saved per-trial prediction arrays; see `audit_summary.md` (10 methods audited, 0 bugs) and `code/UQ_SUMMARY.md` (49 numbers cross-verified against canonical JSON artefacts).

**Base model — Trial 8 (PointNetTransfGAT, dropout 0.2, 100 test graphs, 3,163,500 nodes):**

| Metric | Value |
| ------ | ----- |
| R² | **0.5957** |
| MAE | **3.957 veh/h** |
| RMSE | **7.118 veh/h** |

**Post-hoc UQ on T8:**

| Analysis | Result |
| -------- | ------ |
| MC Dropout (S=30) Spearman ρ (σ vs \|error\|) | **0.4820** pooled; per-graph mean 0.464, 95% CI [0.460, 0.469] |
| Raw interval calibration | k₉₅ = **11.66** vs Gaussian 1.96 (severely overconfident) |
| Regression σ-scaling (T\* = 2.887) | ECE 0.356 → **0.034** (−90.5%); 1σ coverage 32.7% → 68.0%; k₉₅ → 4.04 |
| Split conformal (scenario-level, seed 42) | PICP₉₀ = **90.02%** (q₉₀ = 9.920); PICP₉₅ = **95.01%** (q₉₅ = 14.677) |
| Adaptive conformal (σ-normalised, q = 7.71) | Conditional coverage across σ-deciles: [59.0%, 98.1%] → **[83.7%, 96.4%]** |
| Selective prediction (50% most confident retained) | MAE −**41.2%** → 2.32 veh/h (25%: −54.5%; 10%: −73.4%) |
| Error detection AUROC | **0.7548** (top-10% errors), 0.7324 (top-20%) |

**Uncertainty-aware training extensions (isolate backbone trainability):**

| Trial | Design | R² | Gates | Verdict |
| ----- | ------ | -- | ----- | ------- |
| T9 | Heteroscedastic head, frozen backbone | 0.4991 | 2/3 pass (R² ≥ 0.55 fails) | Partial — k₉₅ improves 4× to 2.84; 99.85% aleatoric-dominated |
| T10 | CQR head, **unfrozen** backbone | 0.4057 | 3/6 fail | **Negative** — pinball gradients destroy MSE representations |
| T11 | CQR head, **frozen** backbone | 0.5835 | **6/6 pass** | **Positive** — MAE 4.302 veh/h; single deterministic pass |

**Ensembles & baselines:**

| Model | R² | Spearman ρ |
| ----- | -- | ---------- |
| Deep Ensemble (5 members, seeds {42,137,256,389,512}) | **0.6841** (+14.8% vs T8) | 0.3997 |
| XGBoost (tabular baseline) | 0.7414 | — |
| Random Forest (tabular baseline) | 0.6612 | — |
| MLP (tabular baseline) | 0.4928 | — |
| Multi-model ensemble (T2/T5/T6/T7/T8, R²-weighted) | 0.5656 | 0.4333 |

**Key caveats reported in the thesis:**

- Stratified by |Δv| quartile, MC Dropout ranking falls from ρ = 0.721 (Q1, zero-effect segments) to **ρ = 0.100 (Q4)**, while MAE rises 1.24 → 10.08 veh/h — the uncertainty signal is weakest exactly where policy effects are largest.
- 88.7% of test nodes have Δv = 0, which flattens AUROC and selective-prediction metrics.
- Tree baselines beat the GNN on point accuracy; the thesis contribution is the per-prediction UQ pipeline, which default tree models do not provide.
- Cross-replication on Trial 7 (dropout 0.3): ρ = 0.4437, k₉₅ = 16.15, AUROC = 0.7416 — qualitatively unchanged.

---

## Repository Structure

```
document/                    Thesis document (submitted version)
  main.tex, settings.tex     LaTeX root + metadata
  chapters/                  Chapters 01-07 + appendix (master table)
  pages/                     Cover, title, abstracts (EN/DE), acknowledgments
  figures/new/               All thesis figures (PDF + PNG)
  main.pdf                   Compiled thesis (submitted May 15, 2026)
  Zamin_Quadri_Master_Thesis.docx
code/
  scripts/gnn/               GNN architectures (PointNetTransfGAT, frozen heteroscedastic/CQR variants), losses
  scripts/training/          Training pipelines (base trials, deep ensemble, heteroscedastic, CQR)
  scripts/data_preprocessing/ MATSim -> PyG graph conversion
  scripts/misc/              Figure generation, batch analyses, verification
  colab_*.ipynb              Colab notebooks (UQ master, σ-scaling, ensembles, RF baseline)
  docs/                      Script-level documentation (preprocessing, GNN, training)
  UQ_SUMMARY.md              Full verified results summary (49 cross-checked numbers)
audit_summary.md             Independent UQ implementation audit (10 methods, 0 bugs)
THESIS_FIX_PLAN.md           Pre-submission revision plan (80 issues, all applied)
THESIS_REVIEW_NOTES.md       Section-by-section review + defence Q&A prep
thesis_overleaf.zip          Overleaf source archive
```

> **Data note:** Training data (~4.8 GB), dataloaders, benchmark artefacts, and trained model
> checkpoints are **not** included in this repository (kept locally; GitHub size/LFS limits).
> All code, notebooks, figures, and the full thesis document are included.

## Compiling the Thesis

```bash
cd document
pdflatex main.tex && biber main && pdflatex main.tex && pdflatex main.tex
```

## Environment

```bash
conda env create -f code/environment-minimal.yml
conda activate traffic-gnn
```

## Builds On

> Natterer et al. (2025). *Machine Learning Surrogates for Agent-Based Models in Transportation Policy Analysis.* Transportation Research Part C, 180, 105360.

This thesis reuses that work's MATSim simulation corpus and preprocessing pipeline, and contributes the UQ evaluation framework, calibration analysis, uncertainty-aware training extensions, and cross-replication study.

## License

Submitted as a Master's thesis at the Technical University of Munich. Contact the author for reuse permissions.
