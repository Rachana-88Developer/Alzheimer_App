from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.post("", response_model=schemas.PatientOut, status_code=201)
def create_patient(payload: schemas.PatientCreate,
                   db: Session = Depends(get_db),
                   _: models.User = Depends(get_current_user)):
    patient = models.Patient(**payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@router.get("", response_model=List[schemas.PatientOut])
def list_patients(db: Session = Depends(get_db),
                  _: models.User = Depends(get_current_user)):
    return db.query(models.Patient).order_by(models.Patient.created_at.desc()).all()


@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int,
                db: Session = Depends(get_db),
                _: models.User = Depends(get_current_user)):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
