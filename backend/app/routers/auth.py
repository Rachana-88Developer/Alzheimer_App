from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..security import verify_password, create_access_token
from ..deps import require_roles, get_current_user
from .. import models, schemas

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.username, role=user.role.value)
    return schemas.Token(access_token=token, role=user.role.value, username=user.username)


@router.get("/me", response_model=schemas.UserOut)
def me(user: models.User = Depends(get_current_user)):
    return schemas.UserOut(
        id=user.id, username=user.username,
        full_name=user.full_name, role=user.role.value)


@router.post("/users", response_model=schemas.UserOut, status_code=201)
def create_user(payload: schemas.UserCreate,
                db: Session = Depends(get_db),
                _: models.User = Depends(require_roles("admin"))):
    if db.query(models.User).filter(models.User.username == payload.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    try:
        role = models.Role(payload.role)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid role")
    from ..security import hash_password
    user = models.User(
        username=payload.username, full_name=payload.full_name,
        hashed_password=hash_password(payload.password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return schemas.UserOut(
        id=user.id, username=user.username,
        full_name=user.full_name, role=user.role.value)
