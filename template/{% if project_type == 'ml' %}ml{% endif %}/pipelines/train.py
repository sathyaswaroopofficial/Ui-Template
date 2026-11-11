"""Train a model.  Usage:  uv run python ml/pipelines/train.py --config ml/configs/config.yaml"""

import argparse
import json
import logging

from ml_core.training.trainer import train
from ml_core.utils.config import load_config


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="ml/configs/config.yaml")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    report = train(load_config(args.config))
    print(json.dumps(report["metrics"], indent=2))

    if report["metrics"]["accuracy"] <= report["metrics"]["baseline_accuracy"]:
        raise SystemExit("Model did not beat the baseline; not fit for promotion.")


if __name__ == "__main__":
    main()
