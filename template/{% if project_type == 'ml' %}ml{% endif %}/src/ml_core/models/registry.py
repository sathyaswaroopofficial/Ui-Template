"""Model name -> estimator factory. Add new models here and select them in config."""

from collections.abc import Callable
from typing import Any

from sklearn.base import ClassifierMixin
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

MODELS: dict[str, Callable[..., ClassifierMixin]] = {
    "baseline": lambda **p: DummyClassifier(strategy="most_frequent", **p),
    "logistic_regression": lambda **p: LogisticRegression(max_iter=1000, **p),
    "random_forest": lambda **p: RandomForestClassifier(**p),
}


def build_model(name: str, params: dict[str, Any] | None = None) -> ClassifierMixin:
    if name not in MODELS:
        raise ValueError(f"Unknown model '{name}'. Available: {sorted(MODELS)}")
    return MODELS[name](**(params or {}))
