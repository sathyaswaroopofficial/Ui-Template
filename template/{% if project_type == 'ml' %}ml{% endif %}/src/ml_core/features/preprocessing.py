"""Preprocessing defined once. It is saved inside the model pipeline, so serving
applies exactly the same transforms as training (no training/serving skew)."""

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_preprocessor() -> Pipeline:
    return Pipeline([("scale", StandardScaler())])
