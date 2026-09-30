from sqlalchemy.orm import Session
from .config import settings
from .security import hash_password
from . import models

DEFAULT_USERS = [
    ("admin", "Administrator", "admin123", models.Role.admin),
    ("doctor", "Dr. Default", "doctor123", models.Role.doctor),
    ("staff", "Staff Member", "staff123", models.Role.staff),
]


def seed_users(db: Session) -> None:
    if not settings.SEED_DEFAULT_USERS:
        return
    for username, full_name, password, role in DEFAULT_USERS:
        exists = db.query(models.User).filter(models.User.username == username).first()
        if not exists:
            db.add(models.User(
                username=username,
                full_name=full_name,
                hashed_password=hash_password(password),
                role=role,
            ))
    
    # Seed default demonstration patient if DB empty
    patient_exists = db.query(models.Patient).first()
    if not patient_exists:
        p1 = models.Patient(
            full_name="John Doe",
            age=72,
            gender="Male",
            education_years=14,
            medical_history="Hypertension, Mild memory complaints",
            family_history="Maternal grandfather diagnosed with Alzheimer's",
            medications="Lisinopril 10mg"
        )
        p2 = models.Patient(
            full_name="Eleanor Vance",
            age=68,
            gender="Female",
            education_years=16,
            medical_history="Type 2 Diabetes",
            family_history="No family history of dementia",
            medications="Metformin 500mg"
        )
        db.add_all([p1, p2])

    db.commit()

