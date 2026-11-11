"""Train a model from a Config and save the artifact + metrics."""

import json
import logging
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline

from ml_core.data.loading import load_dataset, split
from ml_core.evaluation.metrics import compute_metrics
from ml_core.features.preprocessing import build_preprocessor
from ml_core.models.registry import build_model
from ml_core.utils.config import Config
from ml_core.utils.seed import set_seed

logger = logging.getLogger(__name__)


def train(cfg: Config) -> dict:
    set_seed(cfg.seed)
    x, y = load_dataset(cfg.data, cfg.seed)
    x_train, x_test, y_train, y_test = split(x, y, cfg.data.test_size, cfg.seed)

    pipeline = Pipeline(
        [
            ("preprocess", build_preprocessor()),
            ("model", build_model(cfg.model.name, cfg.model.params)),
        ]
    )
    pipeline.fit(x_train, y_train)
    metrics = compute_metrics(y_test, pipeline.predict(x_test))

    baseline = build_model("baseline").fit(x_train, y_train)
    metrics["baseline_accuracy"] = compute_metrics(y_test, baseline.predict(x_test))["accuracy"]

    version = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    out = Path(cfg.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    artifact = {"pipeline": pipeline, "version": version, "n_features": cfg.data.n_features}
    joblib.dump(artifact, out / "model.joblib")
    report = {"version": version, "metrics": metrics, "config": asdict(cfg)}
    (out / "metrics.json").write_text(json.dumps(report, indent=2))

    logger.info("Trained %s v%s: %s", cfg.model.name, version, metrics)
    return report
