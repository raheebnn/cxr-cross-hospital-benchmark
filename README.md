# Directional asymmetry in cross-dataset transfer of chest radiograph classifiers

![python](https://img.shields.io/badge/python-3.8%2B-blue)
![pytorch](https://img.shields.io/badge/PyTorch-2.4-ee4c2c)
![license](https://img.shields.io/badge/license-MIT-green)
![notebooks](https://github.com/USER/cxr-directional-asymmetry/actions/workflows/check-notebooks.yml/badge.svg)

Code for a patient-clustered benchmark of how chest X-ray classifiers transfer between three public collections:
**NIH ChestX-ray14 (A)**, **CheXpert (B)** and **VinBigData / VinDr-CXR (C)**.

- Models: DenseNet121, ConvNeXt-T, ViT-S (3 seeds each, 162 runs) and a logistic-regression baseline
- Training sets: A, B, C, A+B, A+C, B+C
- Pooled-source methods: ERM (natural and balanced sampling), DANN, CORAL, GroupDRO
- Statistics: paired two-level cluster bootstrap (patients and seeds, 2,000 replicates), Holm correction within contrast families, +/-0.01 AUROC equivalence margin

## Headline results

| Question | Result |
|---|---|
| Is transfer symmetric between NIH and CheXpert? | No. DenseNet121 macro-AUROC 0.813 (NIH to NIH) falls to 0.713 (NIH to CheXpert), but 0.804 falls only to 0.785 in the reverse direction. Asymmetry 0.081 [95% CI 0.065, 0.097]; ConvNeXt-T 0.077, ViT-S 0.073 |
| Is it a training-set-size effect? | No. Size effect 0.000 [-0.004, 0.005]. Within view strata the asymmetry keeps its sign but shrinks; only DenseNet121 on PA images stays significant after Holm correction |
| Do DANN, CORAL or GroupDRO beat natural-sampling ERM? | No. 0 of 36 contrasts positive, 17 significantly negative. GroupDRO collapsed onto one hospital in all 27 runs |
| Does ensembling single-hospital models beat one pooled model? | No at NIH and CheXpert (-0.014 to -0.030 AUROC) |
| Does recalibration help? | Yes. Platt scaling on 500 labelled target images cut ECE from 0.080 to 0.022 (pooled) and 0.105 to 0.020 (single source) |
| Hospital identifiable from images? | Yes. 0.934 balanced accuracy from 32 simple descriptors (chance 0.333) |

Labels, case mix and preprocessing differ between the collections, so the asymmetry is an empirical regularity
of these datasets, not a demonstrated acquisition effect.

## Quick start

```bash
git clone https://github.com/USER/cxr-directional-asymmetry && cd cxr-directional-asymmetry
pip install -r requirements.txt          # then install the CUDA build of PyTorch from pytorch.org
python scripts/find_hardcoded_paths.py   # lists G:\ paths; add --replace G: D:/cxr to rewrite them
jupyter lab                              # start with notebooks/03_analysis/11_FINAL_master_analysis_code_only.ipynb
```

Data are not included: see [docs/DATA.md](docs/DATA.md).

## Repository layout

```
notebooks/
  01_data_prep/   NIH preparation (official test list, patient split, 224-px cache)
  02_training/    every training run of the study, one notebook per part of the grid
  03_analysis/    Stage-2 ensemble test, first consolidation, FINAL master analysis
  archive/        older versions of notebooks, kept for provenance
requirements.txt
docs/DATA.md        data sources, splits, derived files
scripts/           helper to find and rewrite hard-coded paths
.github/           CI: notebooks valid, no outputs committed
```

## Notebook map

| Notebook | What it does |
|---|---|
| `01_data_prep/01_nih_prep_and_densenet_chexpert_eval` | NIH split and cache; DenseNet121 evaluation on CheXpert |
| `01_data_prep/01b_chexpert_extraction_and_densenet_chexpert` | CheXpert mirror extraction, U-zeros labels, patient split; DenseNet121 on CheXpert |
| `02_training/02_densenet_nih_to_chexpert` | DenseNet121 trained on NIH, evaluated on CheXpert |
| `02_training/03_convnext_single_site_and_target_val` | ConvNeXt-T single-site runs, target-validation pools |
| `02_training/04_full_transfer_grid_incl_vinbigdata` | Full transfer grid including VinBigData as source |
| `02_training/05_densenet_AplusB_dg_test_on_vinbigdata` | DenseNet121 A+B with ERM, balanced ERM, DANN, CORAL, GroupDRO; tested on C |
| `02_training/06_convnext_dg_pooled` | ConvNeXt-T DG runs on pooled sets |
| `02_training/07_vit_s_single_pooled_dg` | ViT-S single-site, pooled and DG runs |
| `02_training/08_stage3_equal_budget_tuning` | Stage 3: six-trial random search per method, DenseNet121, A+B to C |
| `02_training/09_size_control_and_composition` | Size control (8 random 77,353-image CheXpert subsets) and source-composition runs |
| `02_training/10_densenet_groupdro_AplusC_BplusC` | DenseNet121 GroupDRO on A+C and B+C (7 epochs, 3 seeds) |
| `03_analysis/09_stage2_ensemble_preregistered` | Stage 2: cross-source ensemble vs pooled model (plan hash-stamped before analysis) |
| `03_analysis/10_master_v2_first_consolidation` | First consolidation: transfer matrices, gaps, asymmetry, calibration |
| `03_analysis/11_FINAL_master_analysis_code_only` | **Final analysis.** Reads all archived predictions, recomputes every table and figure |
| `03_analysis/11b_FINAL_master_analysis_with_documentation` | Same analysis with the long markdown documentation, but without the last Grad-CAM cells (8.6b to 8.8) |

Run order: 01 and 01b, then 02 to 10 in `02_training` (the size-control and GroupDRO notebooks need the earlier runs), then `03_analysis/09`, then 11. Notebook 11 can also retrain missing
configurations itself (`CXR_RUN_TRAINING=1`).

All notebooks are committed **without outputs** (kernel outputs were 46 MB for the final notebook).

## Data (not included, details in docs/DATA.md)

Download from the providers and respect each data-use agreement:

- NIH ChestX-ray14: https://nihcc.app.box.com/v/ChestXray-NIHCC
- CheXpert: https://stanfordmlgroup.github.io/competitions/chexpert/
- VinBigData Chest X-ray Abnormalities Detection (Kaggle release of VinDr-CXR): https://www.kaggle.com/competitions/vinbigdata-chest-xray-abnormalities-detection

Preprocessing: grayscale, 224x224 bilinear resize, replicated to 3 channels, ImageNet normalisation,
random horizontal flip only. VinBigData DICOM is converted once to an 8-bit cache (needs `pydicom`).

## Paths: edit before running

The notebooks were written on Windows and use hard-coded paths such as `G:\nih_split.csv`
and `G:\runs`. Run `python scripts/find_hardcoded_paths.py` to list them, and edit them or use `--replace`. The final notebook (11) reads
configuration from environment variables instead:

```
CXR_DATA_ROOT   folder with derived data files (nih_split.csv, chexpert_final_clean.csv, *_224.u8 caches)
CXR_RUNS        folder with run outputs (fair_ens/, vit/, convnext_dg/, dg/, vinbig/, stage3/, ...)
CXR_PROFILE     full | fast | smoke
CXR_RUN_TRAINING, CXR_RUN_KFOLD, CXR_RUN_GPU, CXR_RUN_BENCH, CXR_PRETRAINED, CXR_SHOW_FIGURES, CXR_OUT_NAME
```

Notebook 11 documents the full expected folder layout in its first cells.

## Environment

Reported runs: Python 3.8.20, PyTorch 2.4.1 (CUDA 12.1), timm 1.0.24, statsmodels 0.14.1,
one NVIDIA RTX 4070 SUPER, about 169 GPU-hours. The final notebook states Python 3.10 or newer.

```
pip install -r requirements.txt
# install the CUDA build of PyTorch that matches your driver from https://pytorch.org
```

Without PyTorch, every statistical analysis in notebook 11 still runs from archived predictions.

## Training recipe

ImageNet-pretrained backbones from `timm` (`convnext_tiny.fb_in1k`, `vit_small_patch16_224.augreg_in21k_ft_in1k`,
DenseNet121), six-output head, masked BCE, AdamW, cosine schedule, batch 64, mixed precision, 7 epochs, seeds 0, 1, 2.
DenseNet121 and ConvNeXt-T: lr 1e-4, weight decay 1e-4. ViT-S: lr 5e-5, weight decay 0.05, 300 warm-up steps,
gradient clipping 1.0, stochastic depth 0.1. Best epoch by mean source-validation AUROC.
DANN lambda 0.1, CORAL lambda 1.0, GroupDRO eta 0.01.

## Known gaps

One notebook named in the provenance table of notebook 11 is not in this repository:

- `vinbig_pipeline_fixed`: VinBigData labels (at least 2 of 3 radiologists), DICOM to 224-px cache.

The VinBigData label rule and cache are also built in `02_training/05_densenet_AplusB_dg_test_on_vinbigdata`
and rebuilt by notebook 11 (section 2.2) from raw data.

## Paper

Not included in this repository.

## Citation

See `CITATION.cff`.

## License

MIT for the code (see `LICENSE`). The datasets keep their own licenses.
