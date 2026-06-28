"""Clinical scoring engine.

Normalizes and interprets cognitive/functional assessment scores into
standardized severity bands used downstream by feature engineering.
"""
from typing import Dict


def mmse_band(score: float) -> str:
    if score >= 27:
        return "normal"
    if score >= 24:
        return "mild_concern"
    if score >= 19:
        return "mild"
    if score >= 10:
        return "moderate"
    return "severe"


def moca_band(score: float) -> str:
    if score >= 26:
        return "normal"
    if score >= 18:
        return "mci"
    if score >= 10:
        return "moderate"
    return "severe"


def adl_band(score: float) -> str:
    # Higher ADL score = more impairment in this system (0 independent, 100 dependent)
    if score <= 20:
        return "independent"
    if score <= 50:
        return "partial_dependence"
    return "dependent"


def compute_scores(assessment) -> Dict[str, str]:
    """Return interpreted bands for the three core instruments."""
    return {
        "mmse_band": mmse_band(assessment.mmse_score),
        "moca_band": moca_band(assessment.moca_score),
        "adl_band": adl_band(assessment.adl_score),
    }
