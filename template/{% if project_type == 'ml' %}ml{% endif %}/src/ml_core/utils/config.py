"""Typed config loaded from YAML. Experiments differ by config file, not by code."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class DataConfig:
    n_samples: int = 1000
    n_features: int = 4
    n_classes: int = 2
    test_size: float = 0.2


@dataclass
class ModelConfig:
    name: str = "logistic_regression"
    params: dict[str, Any] = field(default_factory=dict)


@dataclass
class Config:
    seed: int = 42
    output_dir: str = "models"
    data: DataConfig = field(default_factory=DataConfig)
    model: ModelConfig = field(default_factory=ModelConfig)


def load_config(path: str | Path, overrides: dict[str, Any] | None = None) -> Config:
    raw: dict[str, Any] = yaml.safe_load(Path(path).read_text()) or {}
    raw.update(overrides or {})
    return Config(
        seed=raw.get("seed", 42),
        output_dir=raw.get("output_dir", "models"),
        data=DataConfig(**raw.get("data", {})),
        model=ModelConfig(**raw.get("model", {})),
    )
