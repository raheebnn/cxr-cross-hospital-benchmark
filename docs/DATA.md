# Data

No data are shipped with this repository. Download each collection from its provider.

| Site | Collection | Source | Use here |
|---|---|---|---|
| A | NIH ChestX-ray14 | https://nihcc.app.box.com/v/ChestXray-NIHCC | official test list; patient-level 90/10 train/val split of the rest |
| B | CheXpert | https://stanfordmlgroup.github.io/competitions/chexpert/ | frontal images; U-zeros labels; patient-level 80/10/10 split |
| C | VinBigData Chest X-ray Abnormalities Detection (VinDr-CXR) | https://www.kaggle.com/competitions/vinbigdata-chest-xray-abnormalities-detection | 15,000 annotated images; positive when at least 2 of 3 radiologists marked the finding; no Edema label |

The CheXpert images in the reported runs came from a Hugging Face mirror, frontal images only.
Check that your copy matches the original release.

## Findings
Cardiomegaly, Edema, Consolidation, Atelectasis, Pneumothorax, Pleural Effusion.
A finding is evaluated only if it is labelled at the test site, seen in training, and has at least five positives and five negatives.

## Derived files (built by the notebooks)

```
nih_split.csv                 NIH metadata with official / split_rev columns
nih_224.u8                    NIH 224-px uint8 cache
chexpert_final_clean.csv      CheXpert labels, patient ids, split
cx_trainval_224.u8, cx_test_224.npy   CheXpert caches
runs/                         predictions, logits, checkpoints, histories
```

## Preprocessing
Grayscale, 224x224 bilinear resize, 3 channels, ImageNet normalisation, random horizontal flip only.
Intensity statistics are deliberately not harmonised between sites.

## Splits
Patient-level everywhere. VinBigData has no patient ids: 12,000 train / 3,000 validation when it is a source, all 15,000 as test when unseen.
