"""Prediction service with SHAP-based explainability.

Loads (and lazily trains) the model artifact, predicts the Alzheimer's stage,
returns per-stage probabilities and per-feature importance for the instance.
"""
import os
import threading
from typing import Dict, List, Tuple

import numpy as np
import joblib

from .features import FEATURE_NAMES, STAGES, vector_to_list
from . import train as train_module

_lock = threading.Lock()
_artifact = None


def _load_or_train():
    global _artifact
    if _artifact is not None:
        return _artifact
    with _lock:
        if _artifact is not None:
            return _artifact
        if os.path.exists(train_module.ARTIFACT_PATH):
            _artifact = joblib.load(train_module.ARTIFACT_PATH)
        else:
            _artifact = train_module.train(save=True)
    return _artifact


def ensure_model_ready():
    """Called at startup to load/train eagerly."""
    _load_or_train()


def _feature_importance(model, x_row: np.ndarray) -> Dict[str, float]:
    """Best-effort per-instance importance via SHAP, with fallbacks."""
    try:
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(x_row)
        if isinstance(shap_values, list):
            arr = np.mean([np.abs(sv[0]) for sv in shap_values], axis=0)
        else:
            sv = np.array(shap_values)
            arr = np.abs(sv[0]) if sv.ndim >= 2 else np.abs(sv)
        arr = np.asarray(arr, dtype=float).flatten()
        if arr.shape[0] == len(FEATURE_NAMES):
            total = float(arr.sum()) or 1.0
            return {name: float(arr[i] / total) for i, name in enumerate(FEATURE_NAMES)}
    except Exception:
        pass
    importances = getattr(model, "feature_importances_", None)
    if importances is not None:
        total = float(np.sum(importances)) or 1.0
        return {name: float(importances[i] / total) for i, name in enumerate(FEATURE_NAMES)}
    return {name: 0.0 for name in FEATURE_NAMES}


def predict(features: Dict[str, float]) -> Tuple[str, Dict[str, float], Dict[str, float]]:
    artifact = _load_or_train()
    model = artifact["model"]
    x_row = np.array([vector_to_list(features)], dtype=float)

    proba = model.predict_proba(x_row)[0]
    stages: List[str] = artifact.get("stages", STAGES)
    probabilities = {stages[i]: float(proba[i]) for i in range(len(stages))}
    stage = stages[int(np.argmax(proba))]
    importance = _feature_importance(model, x_row)
    importance = dict(sorted(importance.items(), key=lambda kv: kv[1], reverse=True))
    return stage, probabilities, importance
