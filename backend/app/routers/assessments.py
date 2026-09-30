from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import io
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from .. import models, schemas
from ..scoring import compute_scores
from ..ml.features import build_feature_vector
from ..ml.predict import predict
from ..recommendations import build_recommendations
from ..reports import generate_report

router = APIRouter(prefix="/api", tags=["assessments"])


def _run_pipeline(patient, assessment, db: Session):
    """Scoring -> feature engineering -> ML + PyTorch MRI DL fusion -> recommendations."""
    mri_scan = None
    if assessment.mri_scan_id:
        mri_scan = db.get(models.MRIScan, assessment.mri_scan_id)
        if mri_scan:
            assessment.mri_heatmap_url = mri_scan.heatmap_url
            if assessment.mri_atrophy == 0:
                # Estimate atrophy from confidence / stage
                stage_atrophy = {"Non Demented": 0.15, "Very Mild Demented": 0.38, "Mild Demented": 0.62, "Moderate Demented": 0.85}
                assessment.mri_atrophy = stage_atrophy.get(mri_scan.predicted_stage, 0.3)

    compute_scores(assessment)  # validates/interprets bands
    features = build_feature_vector(patient, assessment)
    stage, probabilities, importance = predict(features)

    # Multimodal Fusion with PyTorch MRI Deep Learning model output if MRI scan attached
    if mri_scan and mri_scan.stage_probabilities:
        mri_probs = mri_scan.stage_probabilities
        fused_probs = {}
        for s in probabilities.keys():
            # Blend 60% tabular clinical scores + 40% MRI Deep Learning scan
            p_tab = probabilities.get(s, 0.0)
            p_mri = mri_probs.get(s, 0.0)
            fused_probs[s] = round(0.60 * p_tab + 0.40 * p_mri, 4)

        # Renormalize
        tot = sum(fused_probs.values()) or 1.0
        fused_probs = {k: round(v / tot, 4) for k, v in fused_probs.items()}
        top_stage = max(fused_probs.items(), key=lambda kv: kv[1])[0]
        stage = top_stage
        probabilities = fused_probs
        importance["mri_brain_scan_atrophy"] = 0.28
        tot_imp = sum(importance.values())
        importance = {k: round(v / tot_imp, 4) for k, v in importance.items()}
        importance = dict(sorted(importance.items(), key=lambda kv: kv[1], reverse=True))

    assessment.predicted_stage = stage
    assessment.stage_probabilities = probabilities
    assessment.feature_importance = importance
    assessment.recommendations = build_recommendations(stage, features)


@router.post("/patients/{patient_id}/assessments", response_model=schemas.AssessmentOut, status_code=201)
def create_assessment(patient_id: int,
                      payload: schemas.AssessmentCreate,
                      db: Session = Depends(get_db),
                      user: models.User = Depends(get_current_user)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    assessment = models.Assessment(patient_id=patient_id, created_by=user.username,
                                   **payload.model_dump())
    _run_pipeline(patient, assessment, db)
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    return assessment



@router.get("/patients/{patient_id}/assessments", response_model=List[schemas.AssessmentOut])
def list_assessments(patient_id: int,
                     db: Session = Depends(get_db),
                     _: models.User = Depends(get_current_user)):
    return (db.query(models.Assessment)
            .filter(models.Assessment.patient_id == patient_id)
            .order_by(models.Assessment.created_at.asc()).all())


@router.get("/assessments/{assessment_id}", response_model=schemas.AssessmentOut)
def get_assessment(assessment_id: int,
                   db: Session = Depends(get_db),
                   _: models.User = Depends(get_current_user)):
    a = db.get(models.Assessment, assessment_id)
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return a


@router.get("/assessments/{assessment_id}/report")
def download_report(assessment_id: int,
                    db: Session = Depends(get_db),
                    _: models.User = Depends(get_current_user)):
    a = db.get(models.Assessment, assessment_id)
    if not a:
        raise HTTPException(status_code=404, detail="Assessment not found")
    patient = db.get(models.Patient, a.patient_id)
    pdf_bytes = generate_report(patient, a)
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=report_{assessment_id}.pdf"})
