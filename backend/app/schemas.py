from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    full_name: str = ""
    password: str
    role: str = "staff"


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    full_name: str
    age: int = Field(ge=0, le=120)
    gender: str
    education_years: int = 0
    medical_history: str = ""
    family_history: str = ""
    medications: str = ""


class PatientOut(PatientCreate):
    id: int

    class Config:
        from_attributes = True


class MRIScanOut(BaseModel):
    id: int
    patient_id: int
    filename: str
    file_format: str
    predicted_stage: str
    confidence_score: float
    stage_probabilities: Dict[str, float]
    heatmap_url: str
    original_url: str

    class Config:
        from_attributes = True


class AssessmentCreate(BaseModel):
    mmse_score: float = Field(ge=0, le=30)
    moca_score: float = Field(ge=0, le=30)
    adl_score: float = Field(ge=0, le=100)
    behaviour_score: float = Field(ge=0, le=100)
    language_score: float = Field(ge=0, le=100)
    attention_score: float = Field(ge=0, le=100)
    executive_score: float = Field(ge=0, le=100)
    mri_atrophy: float = Field(ge=0, le=1, default=0)
    voice_biomarker: float = Field(ge=0, le=1, default=0)
    mri_scan_id: Optional[int] = None


class AssessmentOut(BaseModel):
    id: int
    patient_id: int
    mri_scan_id: Optional[int] = None
    created_by: str
    mmse_score: float
    moca_score: float
    adl_score: float
    behaviour_score: float
    language_score: float
    attention_score: float
    executive_score: float
    mri_atrophy: float
    voice_biomarker: float
    predicted_stage: str
    stage_probabilities: Dict[str, float]
    feature_importance: Dict[str, float]
    explainable_ai: Optional[Dict[str, Any]] = None
    recommendations: List[str]
    mri_heatmap_url: Optional[str] = ""

    class Config:
        from_attributes = True


class AssessmentSubmitRequest(AssessmentCreate):
    patient_id: int


class AssessmentSubmitResponse(BaseModel):
    assessment_id: int
    patient_id: int
    clinical_score: Dict[str, Any]
    mri_prediction: Dict[str, Any]
    explainable_ai: Dict[str, Any]


