import os
import yaml
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from pathlib import Path
from joblib import dump
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

ARTIFACT_DIR = Path("artifacts")
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

def load_params(path: str = "params.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    params = load_params()
    X, y = load_iris(return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        train_size=params.get("train_size", 0.8),
        random_state=params.get("random_state", 42),
        stratify=y
    )

    n_estimators = params.get("n_estimators", 200)
    max_depth = params.get("max_depth", 4)
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=params.get("random_state", 42)
    )

    with mlflow.start_run(run_name="rf-iris"):
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        mlflow.log_params({"n_estimators": n_estimators, "max_depth": max_depth})
        mlflow.log_metric("accuracy", float(acc))

        # Save model locally
        model_path = ARTIFACT_DIR / "model.pkl"
        dump(clf, model_path)
        mlflow.log_artifact(str(model_path), artifact_path="model_local")

        # Log sklearn model into MLflow Model format too
        mlflow.sklearn.log_model(clf, artifact_path="model")

        # Confusion matrix/report as artifacts
        cm = confusion_matrix(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        pd.DataFrame(cm).to_csv(ARTIFACT_DIR / "confusion_matrix.csv", index=False)
        pd.DataFrame(report).to_csv(ARTIFACT_DIR / "classification_report.csv")

        mlflow.log_artifact(str(ARTIFACT_DIR / "confusion_matrix.csv"))
        mlflow.log_artifact(str(ARTIFACT_DIR / "classification_report.csv"))

        # Save run id for convenience
        run_id_path = ARTIFACT_DIR / "latest_run.txt"
        run_id_path.write_text(mlflow.active_run().info.run_id)

    print(f"Training done. Accuracy={acc:.4f}")
    print("Artifacts saved under ./artifacts and logged to MLflow.")

if __name__ == "__main__":
    main()
