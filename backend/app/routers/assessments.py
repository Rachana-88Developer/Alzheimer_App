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


def _run_pipeline(patient, assessment):
    """Scoring -> feature engineering -> ML -> recommendations."""
    compute_scores(assessment)  # validates/interprets bands
    features = build_feature_vector(patient, assessment)
    stage, probabilities, importance = predict(features)
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
    _run_pipeline(patient, assessment)
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
