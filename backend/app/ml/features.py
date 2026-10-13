"""Feature engineering module.

Converts patient + assessment records into the ordered numeric feature
vector consumed by the ML model. The same FEATURE_NAMES ordering is used
at training and inference time.
"""
from typing import Dict, List

FEATURE_NAMES: List[str] = [
    "age",
    "gender",
    "education_years",
    "family_history",
    "medical_history",
    "mmse_score",
    "moca_score",
    "adl_score",
    "behaviour_score",
    "language_score",
    "attention_score",
    "executive_score",
    "mri_atrophy",
    "voice_biomarker",
]

STAGES = ["normal", "mci", "mild", "moderate", "severe"]


def _gender_code(gender: str) -> int:
    g = (gender or "").strip().lower()
    if g in ("f", "female"):
        return 0
    if g in ("m", "male"):
        return 1
    return 2


def _has_text(value: str) -> int:
    cleaned = (value or "").strip().lower()
    return 1 if cleaned and cleaned not in ("none", "n/a", "no") else 0


def build_feature_vector(patient, assessment) -> Dict[str, float]:
    """Return an ordered dict of feature_name -> value."""
    return {
        "age": float(patient.age),
        "gender": float(_gender_code(patient.gender)),
        "education_years": float(patient.education_years or 0),
        "family_history": float(_has_text(patient.family_history)),
        "medical_history": float(_has_text(patient.medical_history)),
        "mmse_score": float(assessment.mmse_score),
        "moca_score": float(assessment.moca_score),
        "adl_score": float(assessment.adl_score),
        "behaviour_score": float(assessment.behaviour_score),
        "language_score": float(assessment.language_score),
        "attention_score": float(assessment.attention_score),
        "executive_score": float(assessment.executive_score),
        "mri_atrophy": float(assessment.mri_atrophy),
        "voice_biomarker": float(assessment.voice_biomarker),
    }


def vector_to_list(features: Dict[str, float]) -> List[float]:
    return [features.get(name, 0.0) for name in FEATURE_NAMES]


def build_multimodal_feature_vector(patient, assessment, mri_scan=None) -> Dict[str, float]:
    """Combines tabular clinical scores with deep learning MRI extracted metrics."""
    vec = build_feature_vector(patient, assessment)
    if mri_scan is not None:
        if getattr(mri_scan, "mri_atrophy", None) is not None and mri_scan.mri_atrophy > 0:
            vec["mri_atrophy"] = float(mri_scan.mri_atrophy)
        if getattr(mri_scan, "confidence_score", None) is not None:
            vec["mri_dl_confidence"] = float(mri_scan.confidence_score)
    return vec


def standardize_vector(features: Dict[str, float]) -> Dict[str, float]:
    """Standardizes feature metrics into normalized [0, 1] range for unified analysis."""
    normalized = {}
    normalized["age"] = (features.get("age", 65.0) - 40.0) / 55.0
    normalized["gender"] = features.get("gender", 0.0) / 2.0
    normalized["education_years"] = features.get("education_years", 12.0) / 22.0
    normalized["family_history"] = features.get("family_history", 0.0)
    normalized["medical_history"] = features.get("medical_history", 0.0)
    normalized["mmse_score"] = (30.0 - features.get("mmse_score", 24.0)) / 30.0
    normalized["moca_score"] = (30.0 - features.get("moca_score", 22.0)) / 30.0
    normalized["adl_score"] = features.get("adl_score", 20.0) / 100.0
    normalized["behaviour_score"] = features.get("behaviour_score", 20.0) / 100.0
    normalized["language_score"] = features.get("language_score", 20.0) / 100.0
    normalized["attention_score"] = features.get("attention_score", 20.0) / 100.0
    normalized["executive_score"] = features.get("executive_score", 20.0) / 100.0
    normalized["mri_atrophy"] = features.get("mri_atrophy", 0.25)
    normalized["voice_biomarker"] = features.get("voice_biomarker", 0.20)
    return {k: round(float(v), 4) for k, v in normalized.items()}

