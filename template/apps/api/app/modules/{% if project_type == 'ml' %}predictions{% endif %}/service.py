from functools import lru_cache
from pathlib import Path

from ml_core.inference import Predictor

from app.core.config import get_settings
from app.core.errors import AppError, ServiceUnavailableError
from app.modules.predictions.schemas import PredictionOut, PredictRequest, PredictResponse


@lru_cache
def _load_predictor(path: str) -> Predictor:
    return Predictor.load(path)


def get_predictor() -> Predictor:
    path = get_settings().model_path
    if not Path(path).exists():
        raise ServiceUnavailableError("No trained model found. Run `make train` first.")
    return _load_predictor(path)


class PredictionService:
    def __init__(self, predictor: Predictor):
        self.predictor = predictor

    def predict(self, req: PredictRequest) -> PredictResponse:
        try:
            preds = self.predictor.predict(req.rows)
        except ValueError as exc:
            raise AppError(str(exc), code="invalid_input", status_code=422) from exc
        return PredictResponse(
            model_version=self.predictor.version,
            predictions=[PredictionOut(label=p.label, confidence=p.confidence) for p in preds],
        )
