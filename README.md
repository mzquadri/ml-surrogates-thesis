# Uncertainty Quantification for Machine Learning Models in Transportation Policy Analysis

**Master's Thesis** | Technical University of Munich | School of Computation, Information and Technology

|                |                                                          |
| -------------- | -------------------------------------------------------- |
| **Author**     | Mohd Zamin Quadri                                        |
| **Programme**  | M.Sc. Mathematics in Science and Engineering             |
| **Supervisor** | Prof. Dr. Stephan Günnemann                              |
| **Advisors**   | Dominik Fuchsgruber, M.Sc., Elena Natterer, M.Sc.        |
| **Submitted**  | May 2026                                                 |

**[Read the thesis (PDF)](document/main.pdf)**

---

## Abstract

Agent-based transport simulations like MATSim are powerful but computationally expensive. GNN surrogates approximate them orders of magnitude faster, yet lack confidence estimates — a critical gap for policy decisions.

This thesis develops a post-hoc uncertainty quantification framework for a GNN surrogate trained on 10,000 MATSim simulations of the Paris Île-de-France road network (31,635 road segments), combining MC Dropout, conformal prediction, calibration diagnostics, selective prediction, and error detection. No retraining is required.

---

## Key Results

| Analysis | Trial 8 | Trial 7 |
| -------- | ------- | ------- |
| Deterministic MAE / RMSE | 3.96 / 7.12 veh/h | — |
| R² | 0.5957 | — |
| MC Dropout Spearman ρ | 0.482 | 0.446 |
| Conformal 90% / 95% coverage | 90.02% / 95.01% | 89.98% / 95.03% |
| ECE (before / after temperature scaling) | 0.269 / 0.048 | — |
| Selective prediction MAE reduction @50% | 41.2% | — |
| Error detection AUROC (top-10%) | 0.7552 | — |

All numbers verified against raw artifacts during the thesis audit.

---

## Repository Structure

```
document/                    Thesis document (LaTeX source + compiled main.pdf + DOCX)
  chapters/                  Chapters 01-07 + appendix
  figures/                   All thesis figures (PDF + PNG)
code/
  scripts/gnn/               GNN architectures (PointNet + Transformer + GAT, EIGN)
  scripts/training/          Training pipeline (deep ensembles, CQR, heteroscedastic)
  scripts/data_preprocessing/ MATSim -> PyG graph conversion
  scripts/misc/              Figure generation, consistency checks, verification
  docs/                      Documentation (data preprocessing, GNN, training)
  colab_*.ipynb              Colab notebooks (UQ master, temperature scaling, ensembles)
thesis_overleaf.zip          Overleaf source archive of the thesis
```

> **Note:** Training data (~4.8 GB), dataloaders, benchmark artifacts, and trained model
> checkpoints are **not** included in this repository (kept locally). All code and the
> full thesis document are included.

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
