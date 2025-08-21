from pathlib import Path

import numpy as np
from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel

app = FastAPI(title="MLOps Quickstart API", version="0.1.0")

MODEL_PATH = Path("artifacts/model.pkl")
_model = None


class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            # In CI/CD environment, return a mock response
            return MockModel()
        _model = load(MODEL_PATH)
    return _model


class MockModel:
    """Mock model for CI/CD testing when artifacts are not available"""
    
    def predict(self, X):
        return [0]  # Default prediction
    
    def predict_proba(self, X):
        return [[1.0, 0.0, 0.0]]  # Default probabilities


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(features: IrisInput):
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
    pred = model.predict(X)[0]
    proba = getattr(model, "predict_proba", lambda x: None)(X)
    proba_list = proba[0].tolist() if proba is not None else None
    return {"prediction": int(pred), "proba": proba_list}
