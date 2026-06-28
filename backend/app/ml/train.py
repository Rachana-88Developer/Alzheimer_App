"""Synthetic dataset generator + model trainer.

Generates a clinically-plausible synthetic dataset and trains a classifier
for Alzheimer's staging (normal -> mci -> mild -> moderate -> severe).

Model choice is selectable via MODEL_TYPE: random_forest | xgboost | lightgbm.
If the optional library is missing, it safely falls back to RandomForest.
The artifact (model + metadata) is saved to ml/artifacts/model.pkl.

Run:  python -m app.ml.train
"""
import os
import numpy as np
import joblib

from .features import FEATURE_NAMES, STAGES

ARTIFACT_DIR = os.path.join(os.path.dirname(__file__), "artifacts")
ARTIFACT_PATH = os.path.join(ARTIFACT_DIR, "model.pkl")
MODEL_TYPE = os.environ.get("MODEL_TYPE", "random_forest")


def _generate_dataset(n: int = 4000, seed: int = 42):
    rng = np.random.default_rng(seed)
    X, y = [], []
    for _ in range(n):
        stage_idx = int(rng.integers(0, len(STAGES)))
        sev = stage_idx / (len(STAGES) - 1)

        age = np.clip(rng.normal(60 + sev * 20, 8), 40, 95)
        gender = rng.integers(0, 3)
        education = np.clip(rng.normal(14 - sev * 5, 3), 0, 22)
        family_history = int(rng.random() < (0.2 + sev * 0.4))
        medical_history = int(rng.random() < (0.2 + sev * 0.4))

        mmse = np.clip(rng.normal(29 - sev * 22, 2.5), 0, 30)
        moca = np.clip(rng.normal(28 - sev * 22, 2.5), 0, 30)
        adl = np.clip(rng.normal(sev * 90, 10), 0, 100)
        behaviour = np.clip(rng.normal(sev * 80, 12), 0, 100)
        language = np.clip(rng.normal(sev * 75, 12), 0, 100)
        attention = np.clip(rng.normal(sev * 78, 12), 0, 100)
        executive = np.clip(rng.normal(sev * 80, 12), 0, 100)
        mri = np.clip(rng.normal(sev * 0.9, 0.12), 0, 1)
        voice = np.clip(rng.normal(sev * 0.85, 0.12), 0, 1)

        X.append([age, gender, education, family_history, medical_history,
                  mmse, moca, adl, behaviour, language, attention,
                  executive, mri, voice])
        y.append(stage_idx)
    return np.array(X, dtype=float), np.array(y, dtype=int)


def _random_forest():
    from sklearn.ensemble import RandomForestClassifier
    return RandomForestClassifier(
        n_estimators=300, max_depth=None, n_jobs=-1, random_state=42)


def _build_model():
    """Build the configured model.

    Falls back to RandomForest if the optional library (xgboost/lightgbm)
    is not installed, so the app runs with the lighter local requirements.
    """
    if MODEL_TYPE == "xgboost":
        try:
            from xgboost import XGBClassifier
            return XGBClassifier(
                n_estimators=300, max_depth=5, learning_rate=0.1,
                subsample=0.9, colsample_bytree=0.9,
                objective="multi:softprob", num_class=len(STAGES),
                eval_metric="mlogloss", tree_method="hist")
        except ImportError:
            print("xgboost not installed; falling back to RandomForest.")
            return _random_forest()
    if MODEL_TYPE == "lightgbm":
        try:
            from lightgbm import LGBMClassifier
            return LGBMClassifier(
                n_estimators=300, max_depth=-1, learning_rate=0.05,
                num_leaves=31, subsample=0.9, colsample_bytree=0.9)
        except ImportError:
            print("lightgbm not installed; falling back to RandomForest.")
            return _random_forest()
    return _random_forest()


def train(save: bool = True):
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X, y = _generate_dataset()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)
    model = _build_model()
    model.fit(X_train, y_train)
    acc = accuracy_score(y_test, model.predict(X_test))

    artifact = {
        "model": model,
        "model_type": MODEL_TYPE,
        "feature_names": FEATURE_NAMES,
        "stages": STAGES,
        "test_accuracy": float(acc),
    }
    if save:
        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        joblib.dump(artifact, ARTIFACT_PATH)
        print(f"Saved model to {ARTIFACT_PATH} (type={MODEL_TYPE}, acc={acc:.3f})")
    return artifact


if __name__ == "__main__":
    train()
