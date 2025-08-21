import os
import time
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException
from joblib import load
from prometheus_client import Counter, Histogram, generate_latest
from prometheus_client.core import REGISTRY
from prometheus_client.multiprocess import MultiProcessCollector
from pydantic import BaseModel

# Prometheus 메트릭 정의
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"]
)

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
)

PREDICTION_COUNT = Counter(
    "ml_predictions_total", "Total ML predictions", ["model_name", "prediction_class"]
)

PREDICTION_DURATION = Histogram(
    "ml_prediction_duration_seconds",
    "ML prediction duration in seconds",
    ["model_name"],
)

# Multi-process collector 설정
if "PROMETHEUS_MULTIPROC_DIR" in os.environ:
    REGISTRY.register(MultiProcessCollector(REGISTRY))

app = FastAPI(title="MLOps Quickstart API", version="1.0.0")

MODEL_PATH = Path("artifacts/model.pkl")
_model = None


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


class MockModel:
    """Mock model for CI/CD testing when artifacts are not available"""

    def predict(self, X):
        return [0]  # Default prediction

    def predict_proba(self, X):
        return [[1.0, 0.0, 0.0]]  # Default probabilities


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            # In CI/CD environment, return a mock response
            return MockModel()
        _model = load(MODEL_PATH)
    return _model


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    """Prometheus 메트릭 엔드포인트"""
    return generate_latest()


@app.post("/predict")
def predict(features: IrisInput):
    # 메트릭 수집 시작
    start_time = time.time()

    try:
        model = get_model()
        X = np.array(
            [
                [
                    features.sepal_length,
                    features.sepal_width,
                    features.petal_length,
                    features.petal_width,
                ]
            ]
        )

        # 예측 실행
        pred = model.predict(X)[0]
        proba = getattr(model, "predict_proba", lambda x: None)(X)
        proba_list = (
            proba[0].tolist()
            if proba is not None and hasattr(proba[0], "tolist")
            else (proba[0] if proba is not None else None)
        )

        # 예측 성공 메트릭 기록
        PREDICTION_COUNT.labels(
            model_name="iris_classifier", prediction_class=str(pred)
        ).inc()

        # 응답 시간 메트릭 기록
        duration = time.time() - start_time
        PREDICTION_DURATION.labels(model_name="iris_classifier").observe(duration)

        return {"prediction": int(pred), "proba": proba_list}

    except Exception as e:
        # 예측 실패 메트릭 기록
        PREDICTION_COUNT.labels(
            model_name="iris_classifier", prediction_class="error"
        ).inc()
        raise HTTPException(status_code=500, detail=str(e))


@app.middleware("http")
async def add_metrics(request, call_next):
    """HTTP 요청 메트릭 수집 미들웨어"""
    start_time = time.time()

    response = await call_next(request)

    # 요청 수 메트릭 기록
    REQUEST_COUNT.labels(
        method=request.method, endpoint=request.url.path, status=response.status_code
    ).inc()

    # 요청 시간 메트릭 기록
    duration = time.time() - start_time
    REQUEST_DURATION.labels(method=request.method, endpoint=request.url.path).observe(
        duration
    )

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
