# AI-Powered Alzheimer's Clinical Decision Support System (CDSS)

A full-stack clinical decision support system that helps clinicians assess and stage Alzheimer's disease using cognitive assessments, clinical scoring, machine learning, and explainable AI.

> **DISCLAIMER:** This software is for educational/research purposes only. It is **not** a medical device and must **not** be used for real clinical diagnosis or treatment decisions.

## Architecture

```
Login (Doctor/Admin/Staff)
  -> Dashboard
     -> Patient Management (registration, medical/family history, medications)
     -> Assessment Module (MMSE, MoCA, ADL/IADL, behaviour, language, attention, executive)
     -> Previous Records (history, reports, MRI, voice, progress graph)
  -> Clinical Scoring Engine (MMSE / MoCA / ADL scores)
  -> Feature Engineering (age, gender, education, history, scores, MRI/voice features)
  -> ML Prediction (RandomForest / XGBoost / LightGBM)
  -> Explainable AI (SHAP / feature importance)
  -> Stage Prediction (Normal -> MCI -> Mild -> Moderate -> Severe)
  -> Recommendation Engine (follow-up / neurologist / MRI / medication review / caregiver advice)
  -> PDF Report Generator
  -> PostgreSQL
```

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, JWT auth
- **ML:** scikit-learn, XGBoost, LightGBM, SHAP
- **Frontend:** React + Vite
- **Reports:** ReportLab (PDF)
- **Infra:** Docker + docker-compose

## Quick Start (Docker - recommended)

Prerequisites: Docker + Docker Compose.

```bash
git clone https://gitlab.com/ishakarnawat25/alzheimers-clinical-support-system.git
cd alzheimers-clinical-support-system
cp .env.example .env
docker compose up --build
```

Then:
- Backend API + docs: http://localhost:8000/docs
- Frontend: http://localhost:5173

The backend automatically trains the ML model on first startup if no model artifact exists, and seeds default users.

### Default login accounts (seeded)

| Role   | Username | Password   |
|--------|----------|------------|
| Admin  | admin    | admin123   |
| Doctor | doctor   | doctor123  |
| Staff  | staff    | staff123   |

> Change these immediately in any non-local environment.

## Manual Local Setup (without Docker)

See `backend/README.md` and `frontend/README.md`.

## Project Layout

```
alzheimers-clinical-support-system/
  backend/        FastAPI app, ML pipeline, scoring, reports
  frontend/       React + Vite UI
  docker-compose.yml
  .env.example
  README.md
```
