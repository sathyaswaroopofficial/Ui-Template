"""Dataset loading and splitting.

The template ships with a synthetic dataset so everything runs out of the box.
Replace `load_dataset` with your real source (files in data/raw, a database, S3...).
"""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from ml_core.utils.config import DataConfig


def load_dataset(cfg: DataConfig, seed: int) -> tuple[np.ndarray, np.ndarray]:
    x, y = make_classification(
        n_samples=cfg.n_samples,
        n_features=cfg.n_features,
        n_informative=min(cfg.n_features, max(2, cfg.n_classes)),
        n_redundant=0,
        n_classes=cfg.n_classes,
        random_state=seed,
    )
    return x, y


def split(x: np.ndarray, y: np.ndarray, test_size: float, seed: int):
    return train_test_split(x, y, test_size=test_size, random_state=seed, stratify=y)
