import enum
from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Float, Text, Enum, JSON
)
from sqlalchemy.orm import relationship
from .database import Base


class Role(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    staff = "staff"


def _now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    full_name = Column(String(128), nullable=False, default="")
    hashed_password = Column(String(256), nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.staff)
    created_at = Column(DateTime(timezone=True), default=_now)


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(128), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(16), nullable=False)
    education_years = Column(Integer, default=0)
    medical_history = Column(Text, default="")
    family_history = Column(Text, default="")
    medications = Column(Text, default="")
    created_at = Column(DateTime(timezone=True), default=_now)

    assessments = relationship("Assessment", back_populates="patient", cascade="all, delete-orphan")


class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False, index=True)
    created_by = Column(String(64), default="")
    created_at = Column(DateTime(timezone=True), default=_now)

    # Raw assessment inputs
    mmse_score = Column(Float, default=0)
    moca_score = Column(Float, default=0)
    adl_score = Column(Float, default=0)
    behaviour_score = Column(Float, default=0)
    language_score = Column(Float, default=0)
    attention_score = Column(Float, default=0)
    executive_score = Column(Float, default=0)
    mri_atrophy = Column(Float, default=0)   # 0-1 normalized hippocampal atrophy proxy
    voice_biomarker = Column(Float, default=0)  # 0-1 normalized speech impairment proxy

    # Prediction outputs
    predicted_stage = Column(String(32), default="")
    stage_probabilities = Column(JSON, default=dict)
    feature_importance = Column(JSON, default=dict)
    recommendations = Column(JSON, default=list)

    patient = relationship("Patient", back_populates="assessments")
