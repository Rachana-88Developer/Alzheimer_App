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
    return [features[name] for name in FEATURE_NAMES]
