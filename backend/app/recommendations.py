"""Recommendation engine.

Maps predicted stage + key features to clinical follow-up suggestions.
Educational use only - not medical advice.
"""
from typing import Dict, List


def build_recommendations(stage: str, features: Dict[str, float]) -> List[str]:
    recs: List[str] = []
    stage = stage.lower()

    if stage == "normal":
        recs.append("Routine annual cognitive follow-up.")
        recs.append("Encourage cognitive, physical and social activity.")
    elif stage == "mci":
        recs.append("Schedule follow-up cognitive assessment in 6 months.")
        recs.append("Consider referral to a neurologist for baseline evaluation.")
        recs.append("Review modifiable risk factors (BP, glucose, sleep).")
    elif stage == "mild":
        recs.append("Refer to a neurologist.")
        recs.append("Order MRI to assess hippocampal/cortical atrophy.")
        recs.append("Begin caregiver education and support planning.")
    elif stage == "moderate":
        recs.append("Urgent neurologist referral.")
        recs.append("Medication review for cognitive symptoms.")
        recs.append("Structured caregiver support and safety assessment at home.")
    elif stage == "severe":
        recs.append("Comprehensive specialist and palliative care planning.")
        recs.append("Full-time caregiver / supervised care evaluation.")
        recs.append("Medication review and management of comorbidities.")

    # Feature-driven add-ons
    if features.get("mri_atrophy", 0) >= 0.6:
        recs.append("High structural atrophy detected: prioritize MRI review.")
    if features.get("voice_biomarker", 0) >= 0.6:
        recs.append("Speech/language biomarker elevated: consider language assessment.")

    return recs
