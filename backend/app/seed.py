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
    db.commit()
