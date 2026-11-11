# ML conventions (ml/)

- Production ML code lives in `src/ml_core/` with tests. Notebooks are for exploration only and are never imported.
- Hyperparameters and paths live in `configs/*.yaml`, never hardcoded in Python.
- Preprocessing is defined ONCE in `ml_core/features` and saved inside the model pipeline, so training and serving use identical transforms.
- The backend serves predictions only through `ml_core.inference.Predictor`.
- Always compare against the baseline model; a new model ships only if it beats production on the test set.
- Set seeds via `ml_core.utils.seed.set_seed` for reproducibility.
- Raw data in `data/raw/` is immutable. Large data and model files are not committed to git (use DVC / a model registry).
