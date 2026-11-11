import pytest
from ml_core.inference import Predictor
from ml_core.training.trainer import train
from ml_core.utils.config import load_config


@pytest.fixture
def trained(tmp_path):
    cfg = load_config("ml/configs/config.yaml", {"output_dir": str(tmp_path)})
    report = train(cfg)
    return tmp_path, report


def test_model_beats_baseline(trained):
    _, report = trained
    assert report["metrics"]["accuracy"] > report["metrics"]["baseline_accuracy"]


def test_predictor_roundtrip(trained):
    out, _ = trained
    predictor = Predictor.load(out / "model.joblib")
    preds = predictor.predict([[0.1, -0.2, 0.3, 0.0]])
    assert len(preds) == 1
    assert 0.0 <= preds[0].confidence <= 1.0


def test_predictor_rejects_wrong_shape(trained):
    out, _ = trained
    predictor = Predictor.load(out / "model.joblib")
    with pytest.raises(ValueError):
        predictor.predict([[1.0, 2.0]])
