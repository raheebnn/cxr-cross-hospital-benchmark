# Contributing

Issues and pull requests are welcome.

- Commit notebooks **without outputs**. Install the hook once: `pip install pre-commit && pre-commit install`.
- Do not commit data, images, checkpoints or prediction files (`.gitignore` blocks the common ones).
- Do not commit absolute paths to your own machine. Run `python scripts/find_hardcoded_paths.py` to check.
- Respect the data-use terms of NIH ChestX-ray14, CheXpert and VinDr-CXR.
