import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import Base, engine, SessionLocal
from .seed import seed_users
from .routers import auth, patients, assessments, mri
from .ml.predict import ensure_model_ready


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(os.path.join(STATIC_DIR, "heatmaps"), exist_ok=True)
os.makedirs(os.path.join(STATIC_DIR, "samples"), exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_users(db)
    finally:
        db.close()
    if settings.AUTO_TRAIN_MODEL:
        ensure_model_ready()
    yield


app = FastAPI(title="Alzheimer's CDSS API", version="1.0.0", lifespan=lifespan)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(assessments.router)
app.include_router(mri.router)


@app.get("/health")
def health():
    return {"status": "ok"}

