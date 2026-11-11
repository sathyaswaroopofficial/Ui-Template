"""The ONLY way production code runs the model. Used by the API and batch jobs."""

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np


@dataclass
class Prediction:
    label: int
    confidence: float


class Predictor:
    def __init__(self, pipeline, version: str, n_features: int):
        self.pipeline = pipeline
        self.version = version
        self.n_features = n_features

    @classmethod
    def load(cls, path: str | Path) -> "Predictor":
        artifact = joblib.load(path)
        return cls(artifact["pipeline"], artifact["version"], artifact["n_features"])

    def predict(self, rows: list[list[float]]) -> list[Prediction]:
        x = np.asarray(rows, dtype=float)
        if x.ndim != 2 or x.shape[1] != self.n_features:
            raise ValueError(f"Expected rows with {self.n_features} features each")
        probs = self.pipeline.predict_proba(x)
        classes = self.pipeline.classes_
        return [
            Prediction(label=int(classes[i]), confidence=float(p[i]))
            for p, i in zip(probs, probs.argmax(axis=1), strict=True)
        ]
