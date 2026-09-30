"""FastAPI Router for MRI Brain Scan Processing, Deep Learning Staging & Heatmap Generation."""
import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import get_current_user
from .. import models, schemas
from ..ml.mri_classifier import predict_mri_scan, KAGGLE_MRI_CLASSES
from ..ml.mri_heatmap import generate_mri_heatmap
from ..ml.sample_mri import generate_sample_brain_mri

router = APIRouter(prefix="/api/mri", tags=["mri"])

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
HEATMAP_DIR = os.path.join(STATIC_DIR, "heatmaps")
SAMPLES_DIR = os.path.join(STATIC_DIR, "samples")


@router.post("/upload", response_model=schemas.MRIScanOut)
async def upload_and_analyze_mri(
    patient_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user)
):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    file_format = file.filename.split('.')[-1].upper() if '.' in file.filename else "PNG"

    try:
        # 1. Run Deep Learning PyTorch MRI Staging inference
        res = predict_mri_scan(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Image processing error: {str(e)}")

    # 2. Generate SHAP / Grad-CAM visual brain heatmap
    orig_url, heatmap_url, orig_path, heatmap_path = generate_mri_heatmap(
        res["image_np"], res["predicted_stage"], HEATMAP_DIR
    )

    # 3. Create DB Record
    mri_scan = models.MRIScan(
        patient_id=patient_id,
        filename=file.filename,
        file_path=orig_path,
        file_format=file_format,
        predicted_stage=res["predicted_stage"],
        confidence_score=res["confidence_score"],
        stage_probabilities=res["stage_probabilities"],
        heatmap_path=heatmap_path,
        heatmap_url=heatmap_url,
        original_url=orig_url
    )

    db.add(mri_scan)
    db.commit()
    db.refresh(mri_scan)

    return mri_scan


@router.get("/patient/{patient_id}", response_model=List[schemas.MRIScanOut])
def get_patient_mri_scans(
    patient_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user)
):
    return (
        db.query(models.MRIScan)
        .filter(models.MRIScan.patient_id == patient_id)
        .order_by(models.MRIScan.uploaded_at.desc())
        .all()
    )


@router.get("/samples")
def get_sample_mri_scans(_: models.User = Depends(get_current_user)):
    generate_sample_brain_mri(SAMPLES_DIR)
    samples = [
        {"key": "non_demented", "label": "Non Demented MRI Scan", "stage": "Non Demented", "url": "/static/samples/sample_mri_non_demented.png"},
        {"key": "very_mild", "label": "Very Mild Demented MRI Scan", "stage": "Very Mild Demented", "url": "/static/samples/sample_mri_very_mild.png"},
        {"key": "mild", "label": "Mild Demented MRI Scan", "stage": "Mild Demented", "url": "/static/samples/sample_mri_mild.png"},
        {"key": "moderate", "label": "Moderate Demented MRI Scan", "stage": "Moderate Demented", "url": "/static/samples/sample_mri_moderate.png"},
    ]
    return samples


@router.post("/analyze-sample", response_model=schemas.MRIScanOut)
def analyze_sample_mri(
    patient_id: int = Form(...),
    sample_key: str = Form(...),
    db: Session = Depends(get_db),
    _: models.User = Depends(get_current_user)
):
    patient = db.get(models.Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    generate_sample_brain_mri(SAMPLES_DIR)
    filename = f"sample_mri_{sample_key}.png"
    filepath = os.path.join(SAMPLES_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Sample MRI file not found")

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    res = predict_mri_scan(file_bytes, filename)
    orig_url, heatmap_url, orig_path, heatmap_path = generate_mri_heatmap(
        res["image_np"], res["predicted_stage"], HEATMAP_DIR
    )

    mri_scan = models.MRIScan(
        patient_id=patient_id,
        filename=filename,
        file_path=orig_path,
        file_format="PNG",
        predicted_stage=res["predicted_stage"],
        confidence_score=res["confidence_score"],
        stage_probabilities=res["stage_probabilities"],
        heatmap_path=heatmap_path,
        heatmap_url=heatmap_url,
        original_url=orig_url
    )

    db.add(mri_scan)
    db.commit()
    db.refresh(mri_scan)

    return mri_scan
