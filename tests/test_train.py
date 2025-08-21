import os
import subprocess
from pathlib import Path

def test_training_produces_model(tmp_path, monkeypatch):
    # run training in project root
    assert (Path("src") / "train.py").exists()
    subprocess.run(["python", "src/train.py"], check=True)
    assert Path("artifacts/model.pkl").exists()
